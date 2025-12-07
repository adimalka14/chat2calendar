import type React from "react"
import type {Metadata} from "next"
import {Inter} from "next/font/google"
import {JetBrains_Mono} from "next/font/google"
import {Analytics} from "@vercel/analytics/next"
import {Suspense} from "react"
import {I18nProvider} from "@/hooks/use-i18n"
import "./globals.css"
import {AuthProvider} from "@/hooks/use-auth";

const inter = Inter({
    subsets: ["latin"],
    variable: "--font-inter",
})

const jetbrainsMono = JetBrains_Mono({
    subsets: ["latin"],
    variable: "--font-jetbrains-mono",
})

export const metadata: Metadata = {
    title: "Chat2Calendar - AI Calendar Assistant",
    description:
        "Modern AI chat application for Google Calendar integration. Manage your calendar with natural language.",
    generator: "v0.app",
}

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode
}>) {
    return (
        <html lang="he" dir="rtl" className="dark">
        <body className={`font-sans ${inter.variable} ${jetbrainsMono.variable} antialiased`}>
        <I18nProvider>
            <Suspense fallback={null}>
                <AuthProvider>
                    {children}
                </AuthProvider>
            </Suspense>
        </I18nProvider>
        <Analytics/>
        </body>
        </html>
    )
}
