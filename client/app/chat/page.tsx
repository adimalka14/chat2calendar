"use client";

import { useRef, useEffect } from "react";
import { AuthGuard } from "@/components/auth-guard";
import { useAuth } from "@/hooks/use-auth";
import { useChat } from "@/hooks/use-chat";
import { MobileHeader } from "@/components/mobile-header";
import { ChatMessage as Bubble } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-input";
import { apiClient } from "@/lib/api";

function ChatPage() {
  const { authState } = useAuth();
  const { messages, isLoading, sendMessage, setMessages } = useChat();
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const name = authState.user?.name || "there";
    setMessages([{
      id: "welcome",
      role: "assistant",
      content:
          `Hi ${name}! 👋\nI'm your Calendar assistant.\nTell me what to do:\n- "What do I have next week?"\n- "Create a meeting with Dan tomorrow 3pm"\n- "Move my 10am to 4pm"\n- "Delete the call with Sarah"\n`,
      timestamp: new Date().toISOString(),
    }]);
  }, [authState.user?.name, setMessages]);

  useEffect(() => {
    const token = localStorage.getItem("chat2calendar-token") || "";
    if (token) apiClient.setAuthToken(token);
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
      <div className="h-screen flex flex-col bg-background">
        <MobileHeader />
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map(m => (
                <Bubble
                    key={m.id}
                    message={m}
                    userAvatar={authState.user?.picture}
                    userName={authState.user?.name}
                />
            ))}
            <div ref={endRef} />
          </div>

          <ChatInput
              isLoading={isLoading}
              onSendMessage={(text) => sendMessage(text)}
          />
        </div>
      </div>
  );
}

export default function Page() {
  return (
        <AuthGuard>
          <ChatPage />
        </AuthGuard>
  );
}
