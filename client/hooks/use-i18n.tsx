"use client"

import type React from "react"

import { createContext, useContext, useState, useEffect } from "react"
import type { Locale, Translations } from "@/lib/i18n"
import { getTranslations } from "@/lib/i18n"

interface I18nContextType {
  locale: Locale
  setLocale: (locale: Locale) => void
  t: Translations
  dir: "ltr"
}

const I18nContext = createContext<I18nContextType | undefined>(undefined)

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>("en")

  useEffect(() => {
    // Update document direction and lang when locale changes
    const translations = getTranslations(locale)
    document.documentElement.dir = translations.direction
    document.documentElement.lang = locale
  }, [locale])

  const translations = getTranslations(locale)

  const value = {
    locale,
    setLocale,
    t: translations,
    dir: translations.direction,
  }

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n() {
  const context = useContext(I18nContext)
  if (context === undefined) {
    throw new Error("useI18n must be used within an I18nProvider")
  }
  return context
}
