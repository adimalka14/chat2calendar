export type Locale = "en"

export interface Translations {
  // Navigation
  signIn: string
  signOut: string
  connecting: string
  language: string
  logout: string

  // Landing Page
  title: string
  subtitle: string
  description: string
  startNow: string
  requiresGoogle: string
  poweredByAI: string

  // Features
  naturalChat: string
  naturalChatDesc: string
  fullSync: string
  fullSyncDesc: string
  smartFast: string
  smartFastDesc: string

  // Chat
  typeMessage: string
  send: string
  newChat: string
  chatHistory: string
  typing: string
  hideCalendar: string
  showCalendar: string
  smartAssistant: string

  // Calendar
  myCalendar: string
  today: string
  upcoming: string
  newEvent: string
  noEventsToday: string
  noUpcomingEvents: string
  createNewEvent: string

  // Demo
  howItWorks: string
  demoMessage: string
  demoResponse: string
  demoNote: string

  // Footer
  footerText: string

  // Auth & Profile
  profile: string
  settings: string
  verifying: string
  loading: string

  direction: "ltr"
}

const translations: Record<Locale, Translations> = {
  en: {
    direction: "ltr",

    signIn: "Sign in with Google",
    signOut: "Sign out",
    connecting: "Connecting...",
    language: "Language",
    logout: "Logout",

    title: "Manage your calendar with natural conversation",
    subtitle: "Chat2Calendar - AI Calendar Assistant",
    description:
      "Chat2Calendar connects Google Calendar with advanced AI. Add, edit and delete events simply through natural conversation.",
    startNow: "Start Now - Free",
    requiresGoogle: "Requires Google Account",
    poweredByAI: "Powered by AI",

    naturalChat: "Natural Chat",
    naturalChatDesc: 'Talk to the bot naturally. "Schedule a meeting tomorrow at 3pm" or "What do I have this week?"',
    fullSync: "Full Sync",
    fullSyncDesc: "Direct connection to your Google Calendar. All changes update in real-time.",
    smartFast: "Smart & Fast",
    smartFastDesc: "The bot understands context, remembers preferences and suggests available times automatically.",

    typeMessage: "Type a message...",
    send: "Send",
    newChat: "New Chat",
    chatHistory: "Chat History",
    typing: "Typing...",
    hideCalendar: "Hide Calendar",
    showCalendar: "Show Calendar",
    smartAssistant: "Smart Calendar Assistant",

    myCalendar: "My Calendar",
    today: "Today",
    upcoming: "Upcoming",
    newEvent: "New Event",
    noEventsToday: "No events today",
    noUpcomingEvents: "No upcoming events",
    createNewEvent: "Create new event",

    howItWorks: "How does it work?",
    demoMessage: '"Schedule a meeting with Danny tomorrow at 2pm"',
    demoResponse: "Scheduled meeting with Danny for tomorrow (Jan 15) at 2:00-3:00 PM",
    demoNote: "Event added to your Google Calendar",

    footerText: "Chat2Calendar - Powered by OpenAI and Google Calendar API",

    profile: "Profile",
    settings: "Settings",
    verifying: "Verifying identity...",
    loading: "Loading...",
  },
}

export const getTranslations = (locale: Locale): Translations => {
  return translations[locale]
}

export const getDirection = (locale: Locale): "rtl" | "ltr" => {
  return getTranslations(locale).direction
}
