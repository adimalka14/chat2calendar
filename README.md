# Chat2Calendar

An AI-powered calendar assistant that enables natural language interaction with Google Calendar. Manage your schedule through conversational chat, powered by OpenAI's function calling capabilities.

## Overview

Chat2Calendar bridges the gap between natural conversation and calendar management. Users can create, update, delete, and query calendar events using plain language in Hebrew or English. The system intelligently interprets user intent and performs calendar operations through an AI agent with persistent conversation memory.

## Technologies

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Modern UI component library
- **React Hooks** - Custom state management

### Backend
- **FastAPI** - High-performance Python web framework
- **OpenAI API** - GPT-4 for natural language processing and function calling
- **Google Calendar API** - Calendar CRUD operations
- **Google OAuth2** - Secure authentication
- **Pydantic** - Data validation and settings management
- **httpx** - Async HTTP client for API calls

## Architecture & Usage Flow

### System Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │ ──────> │   Server    │ ──────> │   Google    │
│  (Next.js)  │         │  (FastAPI)  │         │   APIs      │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   OpenAI    │
                       │     API     │
                       └─────────────┘
```

### Request Flow

1. **Authentication**
   - User initiates Google OAuth flow from the frontend
   - Backend exchanges authorization code for access/refresh tokens
   - Tokens are stored and used for subsequent API calls

2. **Chat Interaction**
   - User sends a natural language message (e.g., "Schedule a meeting tomorrow at 3pm")
   - Frontend sends request to `/ai/chat` endpoint with user message and conversation context
   - Backend AI agent processes the message using OpenAI with function calling
   - Agent determines if calendar operations are needed and calls appropriate tools
   - Calendar service executes operations via Google Calendar API
   - Agent formulates a natural language response based on results
   - Response is returned to the frontend and displayed to the user

3. **Memory Management**
   - Conversation history is maintained per user and conversation session
   - Recent messages (last 10) are included in each AI request for context
   - Memory is stored in-memory (can be extended to persistent storage)

### Module Structure

**Backend Modules:**
- `auth/` - OAuth authentication and user management
- `ai/` - AI agent, memory, and chat controllers
- `calendar/` - Google Calendar API integration
- `shared/` - Middleware, utilities, and common components

**Frontend Structure:**
- `app/` - Next.js App Router pages and API routes
- `components/` - React components and UI elements
- `hooks/` - Custom React hooks for state management
- `lib/` - Utilities, API clients, and helpers

## Google Authentication & Calendar Integration

### OAuth2 Flow

The application implements the standard OAuth2 authorization code flow:

1. **Authorization Request**
   - User clicks "Sign in with Google"
   - Frontend redirects to Google's authorization endpoint
   - Required scopes: `openid`, `email`, `profile`, `https://www.googleapis.com/auth/calendar`

2. **Token Exchange**
   - Google redirects back with authorization code
   - Backend exchanges code for access token and refresh token
   - Tokens are securely stored (typically in HTTP-only cookies or secure storage)

3. **Token Management**
   - Access tokens are used for API requests
   - Refresh tokens are used to obtain new access tokens when expired
   - Middleware validates and injects tokens into request context

### Calendar API Integration

The `GoogleCalendarService` provides a clean interface to Google Calendar API:

**Operations:**
- `get_calendars()` - List user's calendars
- `get_events()` - Retrieve events within a time range
- `create_event()` - Create new calendar events
- `update_event()` - Modify existing events
- `delete_event()` - Remove events from calendar

**Features:**
- Automatic timezone handling (RFC3339 format)
- Support for multiple calendars (defaults to "primary")
- Error handling and retry logic
- Async/await for non-blocking operations

## AI Agent: Memory & Function Calling

### Agent Architecture

The `CalendarAgent` class orchestrates the interaction between OpenAI and Google Calendar:

```python
CalendarAgent
├── OpenAI Client (GPT-4)
├── ConversationMemory
└── GoogleCalendarService
```

### Function Calling

The agent uses OpenAI's function calling feature to intelligently decide when and how to interact with the calendar:

**Available Functions:**
1. `list_events` - Query events in a time range
2. `create_event` - Create new calendar events
3. `update_event` - Modify existing events (by ID or search)
4. `delete_event` - Remove events (by ID or search)

**Function Calling Flow:**
1. User message is sent to OpenAI with function definitions
2. Model analyzes intent and decides if tools are needed
3. If tools are required, model returns function call with parameters
4. Agent executes the function call via `GoogleCalendarService`
5. Tool results are sent back to OpenAI
6. Model generates a natural language response incorporating results

### Conversation Memory

The `ConversationMemory` class maintains context across the conversation:

**Features:**
- Per-user, per-conversation message storage
- Automatic message limit (default: 30 messages per conversation)
- Recent message retrieval (last N messages for context)
- In-memory storage (extensible to Redis/database)

**Memory Structure:**
```
{
  user_id: {
    conversation_id: [Message, Message, ...]
  }
}
```

**Usage:**
- Last 10 messages are included in each AI request
- Maintains conversation context for natural follow-ups
- Enables references to previous events and preferences

### System Prompt

The agent uses a carefully crafted system prompt that:
- Instructs the model to handle both Hebrew and English
- Specifies timezone awareness and conversion
- Guides natural language time expression parsing
- Defines event lookup and search strategies
- Sets boundaries for calendar vs. general conversation

### Example Interaction

**User:** "Schedule a meeting with John tomorrow at 2pm"

**Agent Process:**
1. Parses "tomorrow at 2pm" → converts to RFC3339 datetime
2. Calls `create_event` function with parsed parameters
3. Google Calendar API creates the event
4. Agent responds: "I've scheduled a meeting with John for tomorrow (Jan 15) at 2:00-3:00 PM"

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Cloud Project with Calendar API enabled
- OpenAI API key

### Installation

**Backend:**
```bash
cd server
poetry install
poetry run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd client
npm install
npm run dev
```

### Environment Variables

Configure `.env` files with:
- Google OAuth credentials
- OpenAI API key
- Server configuration
- CORS settings

---

*Built with ❤️ using FastAPI, Next.js, and OpenAI*
