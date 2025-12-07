"use client"

import type React from "react"
import { useEffect } from "react"
import { useAuth } from "@/hooks/use-auth"
import { useRouter } from "next/navigation"
import { useI18n } from "@/hooks/use-i18n"

interface AuthGuardProps {
  children: React.ReactNode
  redirectTo?: string
}

export function AuthGuard({ children, redirectTo = "/" }: AuthGuardProps) {
  const { authState } = useAuth()
  const { t } = useI18n()
  const router = useRouter()

  useEffect(() => {
    if (!authState.isLoading && !authState.isAuthenticated) {
      router.replace(redirectTo)
    }
  }, [authState.isLoading, authState.isAuthenticated, redirectTo, router])

  if (authState.isLoading) {
    return (
        <div className="min-h-screen bg-background flex items-center justify-center">
          <div className="text-center space-y-4">
            <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="text-muted-foreground">{t.verifying}</p>
          </div>
        </div>
    )
  }

  if (!authState.isAuthenticated) {
    return null
  }

  return <>{children}</>
}
