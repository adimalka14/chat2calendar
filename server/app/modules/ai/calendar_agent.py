from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from openai import OpenAI

from app.config import settings
from app.modules.calendar.google_calendar_service import GoogleCalendarService
from app.modules.ai.memory import ConversationMemory


def _parse_rfc3339(value: str) -> datetime:
    """
    Accept strings like:
    - 2025-12-04T10:30:00+02:00
    - 2025-12-04T10:30:00
    - 2025-12-04T10:30:00Z

    If no tzinfo -> attach UTC.
    tz_name is kept in the signature for future use but not required here.
    """
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")

    dt = datetime.fromisoformat(value)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt

SYSTEM_PROMPT_TEMPLATE = (
    "You are an assistant that manages the user's Google Calendar.\n"
    "- The user may write in Hebrew or English. Always understand both.\n"
    "- Reply in the same language as the user's last message whenever possible.\n"
    "- Always reason and schedule using the user's local time zone.\n"
    "- The user's time zone is: {user_timezone}.\n"
    "- The current user time is: {current_time_iso}.\n"
    "- ALWAYS convert vague time expressions like 'tomorrow', 'tomorrow evening', "
    "'today at 10:30', or similar natural-language phrases into explicit "
    "RFC3339 start and end when calling tools.\n"
    "\n"
    "EVENT LOOKUP LOGIC:\n"
    "- For creating or listing events: call create_event or list_events with explicit times.\n"
    "- For updating or deleting events:\n"
    "    * Try to rely on user-provided event_id.\n"
    "    * If the user does NOT give an event_id but describes an event, "
    "      you must NOT call list_events yourself.\n"
    "    * Instead, try first pass the user's description (summary/title and/or time range) "
    "      directly to update_event or delete_event with the information that you have.\n"
    "    * The backend will search for the correct event.\n"
    "    * If the backend reports multiple or zero matches, respond to the user "
    "      asking for clarification. Do NOT attempt your own search.\n"
    "\n"
    "- If the user asks something unrelated to the calendar, answer directly without using tools.\n"
)


TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "Get events from the user's Google Calendar in a specific time range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Google Calendar ID. Defaults to 'primary' if omitted.",
                    },
                    "start": {
                        "type": "string",
                        "description": (
                            "Start of the time range in RFC3339 with timezone, "
                            "e.g. 2025-12-05T00:00:00+02:00"
                        ),
                    },
                    "end": {
                        "type": "string",
                        "description": (
                            "End of the time range in RFC3339 with timezone, "
                            "e.g. 2025-12-05T23:59:59+02:00"
                        ),
                    },
                },
                "required": ["start", "end"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Create a new event in the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Google Calendar ID. Defaults to 'primary' if omitted.",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Short title of the event.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional longer description of the event.",
                    },
                    "start": {
                        "type": "string",
                        "description": (
                            "Event start datetime in RFC3339 with timezone, "
                            "e.g. 2025-12-05T09:00:00+02:00"
                        ),
                    },
                    "end": {
                        "type": "string",
                        "description": (
                            "Event end datetime in RFC3339 with timezone, "
                            "e.g. 2025-12-05T10:00:00+02:00"
                        ),
                    },
                },
                "required": ["summary", "start", "end"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_event",
            "description": (
                "Update an existing Google Calendar event. "
                "You can either provide a known event_id, or ask the system "
                "to locate the event by title and time range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Google Calendar ID. Defaults to 'primary' if omitted.",
                    },

                    # --- How to identify which event to update ---
                    "event_id": {
                        "type": "string",
                        "description": (
                            "ID of the event to update. "
                            "Use this when you already know the exact event id."
                        ),
                    },
                    "title": {
                        "type": "string",
                        "description": (
                            "Optional title (or part of the title) used to find the event "
                            "if event_id is not provided. For example: 'meeting with John'."
                        ),
                    },
                    "start": {
                        "type": "string",
                        "description": (
                            "Optional RFC3339 date-time indicating when the existing event "
                            "roughly starts. Used as a search window together with 'end' if "
                            "event_id is not provided."
                        ),
                    },
                    "end": {
                        "type": "string",
                        "description": (
                            "Optional RFC3339 date-time indicating when the existing event "
                            "roughly ends. Used as a search window together with 'start' if "
                            "event_id is not provided."
                        ),
                    },

                    # --- New values to apply to the event ---
                    "new_summary": {
                        "type": "string",
                        "description": "New title/summary for the event.",
                    },
                    "new_description": {
                        "type": "string",
                        "description": "New description for the event.",
                    },
                    "new_start": {
                        "type": "string",
                        "description": (
                            "New start time in RFC3339 with timezone for the event."
                        ),
                    },
                    "new_end": {
                        "type": "string",
                        "description": (
                            "New end time in RFC3339 with timezone for the event."
                        ),
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": (
                "Delete an event from Google Calendar. "
                "You can either provide a known event_id, or ask the system "
                "to locate the event by title and time range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Google Calendar ID. Defaults to 'primary' if omitted.",
                    },

                    # --- How to identify which event to delete ---
                    "event_id": {
                        "type": "string",
                        "description": (
                            "ID of the event to delete. "
                            "Use this when you already know the exact event id."
                        ),
                    },
                    "title": {
                        "type": "string",
                        "description": (
                            "Optional title (or part of the title) used to find the event "
                            "if event_id is not provided."
                        ),
                    },
                    "start": {
                        "type": "string",
                        "description": (
                            "Optional RFC3339 date-time indicating when the existing event "
                            "roughly starts. Used as a search window together with 'end' if "
                            "event_id is not provided."
                        ),
                    },
                    "end": {
                        "type": "string",
                        "description": (
                            "Optional RFC3339 date-time indicating when the existing event "
                            "roughly ends. Used as a search window together with 'start' if "
                            "event_id is not provided."
                        ),
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]


class CalendarAgent:
    """
    High-level agent:
    - Receives a user message.
    - Uses OpenAI function calling to decide whether to call calendar tools.
    - Calls GoogleCalendarService.
    - Returns a natural-language reply.
    - Stores short conversation history in ConversationMemory.
    """

    def __init__(
        self,
        client: OpenAI,
        service: GoogleCalendarService,
        memory: ConversationMemory,
        default_timezone: str = "Asia/Jerusalem",
        model: Optional[str] = None,
    ) -> None:
        self.client = client
        self.service = service
        self.memory = memory
        self.default_timezone = default_timezone
        self.model = model or getattr(settings, "openai_model", "gpt-4.1-mini")

    # ---------- main entry ----------

    async def handle_user_message(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        user_timezone: Optional[str],
        access_token: str,
    ) -> str:
        # keep tz_name as string only (for Google + prompt)
        tz_name = user_timezone or self.default_timezone

        # we work in UTC for our own clock; tz is just metadata
        now = datetime.now(timezone.utc)
        current_time_iso = now.isoformat()

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            user_timezone=tz_name,
            current_time_iso=current_time_iso,
        )

        # history for this conversation
        history = self.memory.get_recent_messages(user_id, conversation_id, limit=10)

        # build messages for first call
        messages: List[Dict[str, Any]] = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        first_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_msg = first_response.choices[0].message
        tool_calls = getattr(assistant_msg, "tool_calls", None) or []

        # no tools -> simple reply
        if not tool_calls:
            reply_content = assistant_msg.content or ""

            self.memory.add_message(user_id, conversation_id, "user", user_message)
            self.memory.add_message(user_id, conversation_id, "assistant", reply_content)

            return reply_content

        # there ARE tool calls
        tool_messages: List[Dict[str, Any]] = []

        for tool_call in tool_calls:
            func_name = tool_call.function.name
            raw_args = tool_call.function.arguments or "{}"

            try:
                args = json.loads(raw_args)
            except Exception:
                args = {}
            print(raw_args, args)
            result = await self._dispatch_tool(
                func_name, access_token, args, tz_name
            )

            tool_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

        # second call with tool results
        second_messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": user_message},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in tool_calls
                ],
            },
            *tool_messages,
        ]

        second_response = self.client.chat.completions.create(
            model=self.model,
            messages=second_messages,
        )
        final_msg = second_response.choices[0].message
        final_content = final_msg.content or ""

        self.memory.add_message(user_id, conversation_id, "user", user_message)
        self.memory.add_message(user_id, conversation_id, "assistant", final_content)

        return final_content

    # ---------- tool dispatch ----------

    async def _dispatch_tool(
        self,
        name: str,
        access_token: str,
        args: Dict[str, Any],
        tz_name: str,
    ) -> Any:
        if name == "list_events":
            return await self._handle_list_events(access_token, args)
        if name == "create_event":
            return await self._handle_create_event(access_token, args, tz_name)
        if name == "update_event":
            return await self._handle_update_event(access_token, args)
        if name == "delete_event":
            return await self._handle_delete_event(access_token, args)
        return {"error": f"Unknown tool: {name}"}

    # ---------- tool handlers ----------

    async def _handle_list_events(
        self,
        access_token: str,
        args: Dict[str, Any],
    ) -> Dict[str, Any]:
        calendar_id = args.get("calendar_id") or "primary"
        start_str = args.get("start")
        end_str = args.get("end")

        if not start_str or not end_str:
            return {"error": "start and end are required"}

        start_dt = _parse_rfc3339(start_str)
        end_dt = _parse_rfc3339(end_str)

        events = await self.service.get_events(
            access_token=access_token,
            calendar_id=calendar_id,
            start_date=start_dt,
            end_date=end_dt,
        )

        simplified: List[Dict[str, Any]] = []
        for e in events:
            simplified.append(
                {
                    "id": e.get("id"),
                    "summary": e.get("summary"),
                    "description": e.get("description"),
                    "htmlLink": e.get("htmlLink"),
                    "start": e.get("start"),
                    "end": e.get("end"),
                }
            )

        return {"events": simplified}

    async def _handle_create_event(
        self,
        access_token: str,
        args: Dict[str, Any],
        tz_name: str,
    ) -> Dict[str, Any]:
        calendar_id = args.get("calendar_id") or "primary"
        summary = args.get("summary")
        start_str = args.get("start")
        end_str = args.get("end")
        description = args.get("description")

        if not summary or not start_str or not end_str:
            return {"error": "summary, start and end are required"}

        start_dt = _parse_rfc3339(start_str)
        end_dt = _parse_rfc3339(end_str)

        event_data: Dict[str, Any] = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": tz_name,
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": tz_name,
            },
        }

        created = await self.service.create_event(
            access_token=access_token,
            calendar_id=calendar_id,
            event_data=event_data,
        )

        if not created:
            return {"error": "Failed to create event"}

        return {"event": created}

    async def _find_events_for_action(
            self,
            access_token: str,
            calendar_id: str,
            title: Optional[str],
            start: Optional[datetime],
            end: Optional[datetime],
    ) -> list:
        """
        Finds candidate events for update/delete.
        - Filters by time
        - Filters by partial title match (tokenized)
        """

        # ---------- Time Range Logic ----------
        if start and end:
            search_start = start
            search_end = end

        elif start and not end:
            # If only a start time was given, search +24 hours around it
            search_start = start - timedelta(hours=2)
            search_end = start + timedelta(hours=6)

        else:
            # Default fallback window: 7 days
            now = datetime.now(timezone.utc)
            search_start = now
            search_end = now + timedelta(days=7)

        # ---------- Fetch events ----------
        events = await self.service.get_events(
            access_token=access_token,
            calendar_id=calendar_id,
            start_date=search_start,
            end_date=search_end,
            max_results=50,
        )

        if not events:
            return []

        # ---------- Title Filtering ----------
        if title:
            title_words = [
                word.lower()
                for word in title.replace("-", " ").replace("_", " ").split()
                if word.strip()
            ]

            def title_matches(event_title: str) -> bool:
                t = event_title.lower()
                # Each keyword must appear somewhere in title
                return all(word in t for word in title_words)

            filtered = [
                e for e in events
                if "summary" in e and title_matches(e["summary"])
            ]

            return filtered

        return events

    async def _handle_delete_event(self, access_token: str, args: Dict[str, Any]) -> Dict[str, Any]:
        calendar_id = args.get("calendar_id", "primary")
        event_id = args.get("event_id")
        title = args.get("title")
        start_str = args.get("start")
        end_str = args.get("end")

        # If event_id already provided → delete directly
        if event_id:
            ok = await self.service.delete_event(access_token, calendar_id, event_id)
            if ok:
                return {
                    "ok": True,
                    "message": "Deleted",
                    "data": {"event_id": event_id},
                }
            return {"ok": False, "message": "Failed to delete event"}

        # Otherwise → find event manually (by title + time window if provided)
        start_dt = _parse_rfc3339(start_str) if start_str else None
        end_dt = _parse_rfc3339(end_str) if end_str else None

        events = await self._find_events_for_action(
            access_token=access_token,
            calendar_id=calendar_id,
            title=title,
            start=start_dt,
            end=end_dt,
        )

        if len(events) == 0:
            return {"ok": False, "message": "No matching event found"}

        if len(events) > 1:
            # Let the model handle the clarification with the user
            return {
                "ok": False,
                "message": "Multiple events match, need a more specific request",
                "data": {
                    "candidates": [
                        {
                            "id": e.get("id"),
                            "summary": e.get("summary"),
                            "start": e.get("start"),
                            "end": e.get("end"),
                        }
                        for e in events
                    ]
                },
            }

        event = events[0]
        event_id = event["id"]

        ok = await self.service.delete_event(access_token, calendar_id, event_id)
        if not ok:
            return {"ok": False, "message": "Failed to delete event"}

        return {
            "ok": True,
            "message": "Deleted",
            "data": {"event_id": event_id},
        }

    async def _handle_update_event(self, access_token: str, args: Dict[str, Any]) -> Dict[str, Any]:
        calendar_id = args.get("calendar_id", "primary")
        event_id = args.get("event_id")
        title = args.get("title")
        start_str = args.get("start")
        end_str = args.get("end")

        # Build patch from *new_* fields only (these are the updated values)
        patch: Dict[str, Any] = {}

        if "new_summary" in args:
            patch["summary"] = args["new_summary"]
        if "new_description" in args:
            patch["description"] = args["new_description"]

        if "new_start" in args:
            new_start_dt = _parse_rfc3339(args["new_start"])
            patch.setdefault("start", {})
            patch["start"]["dateTime"] = new_start_dt.isoformat()
        if "new_end" in args:
            new_end_dt = _parse_rfc3339(args["new_end"])
            patch.setdefault("end", {})
            patch["end"]["dateTime"] = new_end_dt.isoformat()

        # Nothing to update → no point in calling Google
        if not patch:
            return {
                "ok": False,
                "message": "No fields to update (new_* fields are missing)",
            }

        # 1. Direct update by event_id
        if event_id:
            updated = await self.service.update_event(
                access_token=access_token,
                calendar_id=calendar_id,
                event_id=event_id,
                event_data=patch,
            )
            if updated:
                return {
                    "ok": True,
                    "message": "Updated",
                    "data": {"event": updated},
                }
            return {"ok": False, "message": "Failed to update event"}

        # 2. Otherwise, find event to update (by title + time window if provided)
        start_dt = _parse_rfc3339(start_str) if start_str else None
        end_dt = _parse_rfc3339(end_str) if end_str else None

        events = await self._find_events_for_action(
            access_token=access_token,
            calendar_id=calendar_id,
            title=title,
            start=start_dt,
            end=end_dt,
        )

        if len(events) == 0:
            return {"ok": False, "message": "No matching event found"}

        if len(events) > 1:
            return {
                "ok": False,
                "message": "Multiple events match, need a more specific request",
                "data": {
                    "candidates": [
                        {
                            "id": e.get("id"),
                            "summary": e.get("summary"),
                            "start": e.get("start"),
                            "end": e.get("end"),
                        }
                        for e in events
                    ]
                },
            }

        event_id = events[0]["id"]

        updated = await self.service.update_event(
            access_token=access_token,
            calendar_id=calendar_id,
            event_id=event_id,
            event_data=patch,
        )
        if not updated:
            return {"ok": False, "message": "Failed to update event"}

        return {
            "ok": True,
            "message": "Updated",
            "data": {"event": updated},
        }