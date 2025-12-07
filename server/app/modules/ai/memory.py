from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Literal, TypedDict
from uuid import uuid4


Role = Literal["user", "assistant"]


class MessageDict(TypedDict):
    role: Role
    content: str


@dataclass
class Message:
    role: Role
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationMemory:
    """
    Very simple in-memory conversation store.

    Structure:
        {
            user_id: {
                conversation_id: [Message, Message, ...]
            }
        }
    """

    def __init__(self, max_messages_per_conversation: int = 30) -> None:
        self.max_messages_per_conversation = max_messages_per_conversation
        self._store: Dict[str, Dict[str, List[Message]]] = {}

    # ---- conversation management ----

    def start_conversation(self, user_id: str) -> str:
        """
        Create a new empty conversation for this user and return its id.
        """
        conv_id = str(uuid4())
        user_convs = self._store.setdefault(user_id, {})
        user_convs[conv_id] = []
        return conv_id

    def conversation_exists(self, user_id: str, conversation_id: str) -> bool:
        """
        Check if a conversation exists for this user.
        """
        return conversation_id in self._store.get(user_id, {})

    # ---- messages ----

    def add_message(
        self,
        user_id: str,
        conversation_id: str,
        role: Role,
        content: str,
    ) -> None:
        """
        Append a message to a specific user's conversation.
        """
        user_convs = self._store.setdefault(user_id, {})
        messages = user_convs.setdefault(conversation_id, [])

        messages.append(Message(role=role, content=content))

        # keep only last N messages
        if len(messages) > self.max_messages_per_conversation:
            user_convs[conversation_id] = messages[-self.max_messages_per_conversation :]

    def get_recent_messages(
        self,
        user_id: str,
        conversation_id: str,
        limit: int = 10,
    ) -> List[MessageDict]:
        """
        Return the last `limit` messages for this user + conversation,
        in the exact format OpenAI expects: {"role": "...", "content": "..."}.
        """
        user_convs = self._store.get(user_id, {})
        messages = user_convs.get(conversation_id, [])

        recent = messages[-limit:]
        return [
            MessageDict(role=m.role, content=m.content)
            for m in recent
        ]
