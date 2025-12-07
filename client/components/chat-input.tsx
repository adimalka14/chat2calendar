"use client";
import {useState} from "react";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";

export function ChatInput({
                              onSendMessage,
                              isLoading,
                          }: {
    onSendMessage: (text: string) => void;
    isLoading: boolean;
}) {
    const [text, setText] = useState("");

    return (
        <div className="border-t border-border p-3 flex gap-2">
            <Input
                placeholder="Type your request..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter" && text.trim() && !isLoading) {
                        onSendMessage(text.trim());
                        setText("");
                    }
                }}
            />
            <Button
                disabled={!text.trim() || isLoading}
                onClick={() => {
                    if (!text.trim()) return;
                    onSendMessage(text.trim());
                    setText("");
                }}
            >
                {isLoading ? "..." : "Send"}
            </Button>
        </div>
    );
}
