# Chat2Calendar - AI Calendar Assistant

מערכת צ'אט מודרנית לניהול יומן Google Calendar באמצעות בינה מלאכותית.

## תכונות

- 🤖 **צ'אט חכם**: שיחה טבעית בעברית עם בוט AI
- 📅 **אינטגרציה מלאה**: חיבור ישיר ל-Google Calendar
- 🔐 **אבטחה**: התחברות מאובטחת עם Google OAuth
- 📱 **רספונסיבי**: עיצוב מותאם לכל המכשירים
- 🌙 **מצב כהה**: עיצוב מודרני במצב כהה
- ⚡ **מהיר**: ביצועים מעולים עם Next.js 15

## ארכיטקטורה

### Frontend (Next.js)
- **Framework**: Next.js 15 עם App Router
- **UI**: shadcn/ui + Tailwind CSS
- **State Management**: React Hooks מותאמים אישית
- **Authentication**: Google OAuth (מוכן להטמעה)
- **TypeScript**: טיפוסים מלאים לכל המערכת

### Backend (Python FastAPI)
השרת הפייתון שלך צריך לספק את ה-API הבא:

\`\`\`
POST /chat/message - שליחת הודעה לבוט
GET /chat/history - קבלת היסטוריית שיחות
GET /calendar/events - קבלת אירועי יומן
POST /calendar/events - יצירת אירוע חדש
PUT /calendar/events/{id} - עדכון אירוע
DELETE /calendar/events/{id} - מחיקת אירוע
\`\`\`

## התקנה והפעלה

1. **התקן dependencies**:
\`\`\`bash
npm install
\`\`\`

2. **הגדר משתני סביבה**:
\`\`\`bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

3. **הפעל את השרת**:
\`\`\`bash
npm run dev
\`\`\`

4. **הפעל את השרת Python** (בנפרד):
\`\`\`bash
# בתיקיית השרת שלך
uvicorn main:app --reload --port 8000
\`\`\`

## מבנה הפרויקט

\`\`\`
├── app/                    # Next.js App Router
│   ├── chat/              # עמוד הצ'אט
│   ├── api/               # API Routes
│   └── globals.css        # עיצוב גלובלי
├── components/            # קומפוננטות React
│   ├── ui/               # קומפוננטות UI בסיסיות
│   ├── auth-guard.tsx    # הגנת אותנטיקציה
│   ├── chat-*.tsx        # קומפוננטות צ'אט
│   └── landing-hero.tsx  # עמוד נחיתה
├── hooks/                # Hooks מותאמים
│   ├── use-auth.ts       # ניהול אותנטיקציה
│   ├── use-chat.ts       # ניהול צ'אט
│   └── use-calendar.ts   # ניהול יומן
└── lib/                  # ספריות עזר
    ├── api.ts            # לקוח API
    ├── auth.ts           # לוגיקת אותנטיקציה
    └── utils.ts          # פונקציות עזר
\`\`\`

## הרחבות עתידיות

המערכת בנויה להרחבה קלה:

- **אינטגרציות נוספות**: Outlook, Apple Calendar
- **תכונות AI**: סיכום פגישות, הצעות זמנים חכמות
- **שיתוף**: שיתוף יומנים עם צוותים
- **התראות**: התראות חכמות ותזכורות
- **ניתוח**: דוחות ותובנות על השימוש ביומן

## טכנולוגיות

- **Next.js 15** - React Framework
- **TypeScript** - Type Safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI Components
- **Lucide React** - Icons
- **Google OAuth** - Authentication
- **Python FastAPI** - Backend API
- **Google Calendar API** - Calendar Integration
- **OpenAI API** - AI Chat

המערכת מוכנה לפרודקשן ובנויה לפי best practices של פיתוח מודרני.
