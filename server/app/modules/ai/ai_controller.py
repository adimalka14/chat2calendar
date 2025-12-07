from typing import Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel
from openai import OpenAI

from app.config import settings
from app.modules.ai.calendar_agent import CalendarAgent
from app.modules.ai.memory import ConversationMemory
from app.modules.calendar.google_calendar_service import GoogleCalendarService


router = APIRouter()


# ---- singletons ----

openai_client = OpenAI(api_key=settings.openai_api_key)

calendar_service = GoogleCalendarService()
memory = ConversationMemory()

agent = CalendarAgent(
    client=openai_client,
    service=calendar_service,
    memory=memory,
)


# ---- API models ----

class ChatRequest(BaseModel):
    message: str
    timezone: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str


# ---- endpoint ----

@router.post("/ai/message", response_model=ChatResponse)
async def chat_message(req: ChatRequest, request: Request) -> ChatResponse:
    """
    Entry point from the frontend:
    - Receives message + timezone + optional conversation_id.
    - Reads user_id and google_access_token from request.state (middleware).
    - Manages conversation id via memory.
    - Delegates to CalendarAgent.
    """

    user_id = getattr(request.state, "user_id", "demo-user")
    access_token = getattr(request.state, "google_access_token", None)

    if access_token is None:
        # Minimal handling, no heavy validation
        return ChatResponse(
            reply="Google access token is missing. Please connect your Google account.",
            conversation_id=req.conversation_id or "",
        )

    conversation_id = req.conversation_id
    if not conversation_id or not memory.conversation_exists(user_id, conversation_id):
        conversation_id = memory.start_conversation(user_id)

    reply = await agent.handle_user_message(
        user_id=user_id,
        conversation_id=conversation_id,
        user_message=req.message,
        user_timezone=req.timezone,
        access_token=access_token,
    )

    return ChatResponse(
        reply=reply,
        conversation_id=conversation_id,
    )
