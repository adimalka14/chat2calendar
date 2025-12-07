"use client";
import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuth, AuthProvider } from "@/hooks/use-auth";

function AuthCallback() {
  const router = useRouter();
  const { completeCallback } = useAuth();
  const ran = useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;

    (async () => {
      const code = new URLSearchParams(location.search).get("code");
      if (!code) return router.replace("/");

      try {
        await completeCallback(code);
        router.replace("/chat");
      } catch {
        router.replace("/");
      }
    })();
  }, [router, completeCallback]);


  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
        <p>connecting</p>
      </div>
    </div>
  )
}

export default function Page() {
  return (
          <AuthCallback />
  )
}
