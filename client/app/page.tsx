"use client"

import { useAuth } from "@/hooks/use-auth"
import { LandingHero } from "@/components/landing-hero"
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import { useI18n } from "@/hooks/use-i18n"

function HomePage() {
  const { authState, signIn } = useAuth()
  const { t } = useI18n()
  const router = useRouter()

  useEffect(() => {
    if (!authState.isLoading && authState.isAuthenticated) {
      console.log(authState)
      console.log("redirect to chat from home page")
      router.push("/chat")
    }
  }, [authState.isLoading, authState.isAuthenticated, router])

  if (authState.isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-muted-foreground">{authState.isLoading ? t.loading : t.connecting}</p>
        </div>
      </div>
    )
  }

  if (authState.isAuthenticated) {
    return null
  }

  return <LandingHero onSignIn={signIn} isLoading={authState.isLoading} />
}

export default function Page() {
  return (
      <HomePage />
  )
}
