"use client"

import {useState, type ReactNode} from "react"
import {Button} from "@/components/ui/button"
import {Sheet, SheetContent, SheetTrigger} from "@/components/ui/sheet"
import {Calendar, LogOut} from "lucide-react"
import {useI18n} from "@/hooks/use-i18n"
import {useAuth} from "@/hooks/use-auth"

interface MobileHeaderProps {
    onSignIn?: () => void
    isLoading?: boolean
    children?: ReactNode
}

export function MobileHeader({
                                 onSignIn,
                                 isLoading = false,
                                 children,
                             }: MobileHeaderProps) {
    const {t} = useI18n()
    const {authState, signOut} = useAuth()
    const [open, setOpen] = useState(false)
    const handleSignIn = () => {
        if (!onSignIn) return
        onSignIn()
    }

    const handleSignOut = async () => {
        await signOut()
    }

    return (
        <header
            className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-4 py-3 flex items-center justify-between">
                {/* Left: logo / title */}
                <div className="flex items-center gap-2">
          <span className="text-xl font-bold text-foreground">
            Chat2Calendar
          </span>
                </div>

                {/* Right: auth buttons on DESKTOP only */}
                <div className="hidden md:flex items-center gap-2">
                    {onSignIn ? (
                        <Button
                            onClick={handleSignIn}
                            disabled={isLoading}
                            size="sm"
                            className="bg-primary hover:bg-primary/90 text-primary-foreground"
                        >
                            {isLoading ? "Connecting..." : t.signIn}
                        </Button>
                    ) : (
                        authState.isAuthenticated && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={handleSignOut}
                                className="gap-2 text-muted-foreground hover:text-destructive"
                            >
                                <LogOut className="w-4 h-4"/>
                                <span>{t.signOut}</span>
                            </Button>
                        )
                    )}
                </div>

                {/* Mobile menu trigger */}
                <div className="flex md:hidden">
                    <Sheet open={open} onOpenChange={setOpen}>
                        <SheetTrigger asChild>
                            <Button
                                variant="ghost"
                                size="sm"
                                className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center"
                            >
                                <Calendar className="w-5 h-5 text-primary-foreground"/>
                            </Button>
                        </SheetTrigger>

                        <SheetContent side="right" className="w-full p-0 bg-background">
                            {children ? (
                                // If a custom sidebar is passed, let it control its own clicks
                                <div>{children}</div>
                            ) : (
                                <div className="flex flex-col gap-4 pt-6 p-4">
                                    {onSignIn && !authState.isAuthenticated && (
                                        <Button
                                            onClick={() => {
                                                handleSignIn()
                                                setOpen(false)
                                            }}
                                            disabled={isLoading}
                                            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                                            size="lg"
                                        >
                                            {isLoading ? "Connecting..." : t.signIn}
                                        </Button>
                                    )}

                                    {authState.isAuthenticated && (
                                        <Button
                                            variant="ghost"
                                            size="lg"
                                            onClick={async () => {
                                                await handleSignOut()
                                                setOpen(false)
                                            }}
                                            className="w-full gap-2 text-muted-foreground hover:text-destructive justify-start"
                                        >
                                            <LogOut className="w-4 h-4"/>
                                            <span>{t.signOut}</span>
                                        </Button>
                                    )}
                                </div>
                            )}
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </header>
    )
}
