"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Calendar, MessageSquare, Sparkles, Zap } from "lucide-react"
import { useI18n } from "@/hooks/use-i18n"
import { MobileHeader } from "./mobile-header"

interface LandingHeroProps {
  onSignIn: () => void
  isLoading?: boolean
}

export function LandingHero({ onSignIn, isLoading = false }: LandingHeroProps) {
  const { t } = useI18n()

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <MobileHeader onSignIn={onSignIn} isLoading={isLoading} />

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 py-8 md:py-12">
        <div className="max-w-4xl mx-auto text-center space-y-8 md:space-y-12">
          {/* Hero Section */}
          <div className="space-y-4 md:space-y-6">
            <div className="inline-flex items-center gap-2 bg-muted text-foreground px-3 py-1.5 md:px-4 md:py-2 rounded-full text-xs md:text-sm font-medium border border-border">
              <Sparkles className="w-3 h-3 md:w-4 md:h-4" />
              {t.poweredByAI}
            </div>

            <h1 className="text-3xl md:text-4xl lg:text-6xl font-bold text-foreground text-balance leading-tight">
              {t.title}
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed px-4">
              {t.description}
            </p>

            <div className="flex flex-col gap-3 justify-center items-center px-4">
              <Button
                size="lg"
                onClick={onSignIn}
                disabled={isLoading}
                className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-primary-foreground px-6 md:px-8 py-3 text-base md:text-lg"
              >
                {isLoading ? t.connecting : t.startNow}
              </Button>
              <p className="text-xs md:text-sm text-muted-foreground text-center">{t.requiresGoogle}</p>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mt-16">
            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <MessageSquare className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-card-foreground mb-2">{t.naturalChat}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{t.naturalChatDesc}</p>
            </Card>

            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Calendar className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-card-foreground mb-2">{t.fullSync}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{t.fullSyncDesc}</p>
            </Card>

            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-card-foreground mb-2">{t.smartFast}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{t.smartFastDesc}</p>
            </Card>
          </div>

          {/* Demo Preview */}
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-foreground mb-8">{t.howItWorks}</h2>
            <Card className="p-8 bg-card border-border max-w-2xl mx-auto">
              <div className="space-y-4 text-left">
                <div className="bg-primary/10 p-4 rounded-lg">
                  <p className="text-foreground">{t.demoMessage}</p>
                </div>
                <div className="bg-muted p-4 rounded-lg">
                  <p className="text-foreground">{t.demoResponse}</p>
                  <p className="text-muted-foreground text-sm mt-2">{t.demoNote}</p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-muted-foreground text-sm">{t.footerText}</p>
        </div>
      </footer>
    </div>
  )
}
