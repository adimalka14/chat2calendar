"use client"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Bot, User } from "lucide-react"
import { cn } from "@/lib/utils"
import type { ChatMessage as ChatMessageType } from "@/lib/api"

interface ChatMessageProps {
  message: ChatMessageType
  userAvatar?: string
  userName?: string
}

export function ChatMessage({ message, userAvatar, userName }: ChatMessageProps) {
  const isUser = message.role === "user"
  const timestamp = new Date(message.timestamp).toLocaleTimeString("he-IL", {
    hour: "2-digit",
    minute: "2-digit",
  })

  return (
    <div className={cn("flex gap-3 mb-4", isUser ? "flex-row-reverse" : "flex-row")}>
      <Avatar className="w-8 h-8 flex-shrink-0">
        {isUser ? (
          <>
            <AvatarImage src={userAvatar || "/placeholder.svg"} alt={userName || "User"} />
            <AvatarFallback className="bg-primary text-primary-foreground">
              <User className="w-4 h-4" />
            </AvatarFallback>
          </>
        ) : (
          <AvatarFallback className="bg-accent text-accent-foreground">
            <Bot className="w-4 h-4" />
          </AvatarFallback>
        )}
      </Avatar>

      <div className={cn("flex flex-col gap-1 max-w-[80%]", isUser ? "items-end" : "items-start")}>
        <Card
          className={cn(
            "p-3 text-sm leading-relaxed",
            isUser ? "bg-primary text-primary-foreground border-primary" : "bg-card text-card-foreground border-border",
          )}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
        </Card>
        <span className="text-xs text-muted-foreground px-1">{timestamp}</span>
      </div>
    </div>
  )
}
