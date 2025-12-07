"use client";
import { useState, useCallback } from "react";
import { apiClient, type ChatMessageDTO } from "@/lib/api";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessageDTO[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (text: string) => {
    const userMsg: ChatMessageDTO = {
      id: String(Date.now()),
      content: text,
      role: "user",
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    const res = await apiClient.sendAiMessage(text, conversationId);
    if (res.success && res.data) {
      const aiMsg: ChatMessageDTO = {
        id: String(Date.now() + 1),
        content: res.data.reply ?? "OK",
        role: "assistant",
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, aiMsg]);
      if (res.data.conversation_id) {
            setConversationId(res.data.conversation_id);
      }
    } else {
      const errMsg: ChatMessageDTO = {
        id: String(Date.now() + 2),
        content: res.error ?? "Something went wrong.",
        role: "assistant",
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errMsg]);
    }
    setIsLoading(false);
  }, [conversationId]);

  return { messages, isLoading, sendMessage, setMessages };
}
