# Chat2Calendar Server Architecture

## Overview
A modular monolithic FastAPI server that provides Google Calendar integration with AI-powered natural language processing. The server acts as a mediator between users and Google Calendar, with OpenAI integration for intelligent calendar operations.

## Architecture Pattern
**Modular Monolith with Controller-Service Pattern**

- **Controllers**: Handle HTTP requests/responses, validation, and call services
- **Services**: Implement business logic, integrate with external APIs
- **Models**: Define data structures and validation schemas
- **Shared**: Common utilities, exceptions, middleware, and database connections

## Project Structure
```
server/
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Lock file (auto-generated)
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker setup
├── README.md
├── ARCHITECTURE.md            # This file
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── dependencies.py        # FastAPI dependencies
│   │
│   ├── modules/               # Feature modules
│   │   ├── auth/              # Authentication module
│   │   │   ├── controllers/
│   │   │   │   └── auth_controller.py
│   │   │   ├── services/
│   │   │   │   ├── auth_service.py
│   │   │   │   └── google_oauth_service.py
│   │   │   └── models/
│   │   │       ├── user.py
│   │   │       └── auth_requests.py
│   │   │
│   │   ├── calendar/          # Calendar module
│   │   │   ├── controllers/
│   │   │   │   └── calendar_controller.py
│   │   │   ├── services/
│   │   │   │   ├── calendar_service.py
│   │   │   │   └── google_calendar_service.py
│   │   │   └── models/
│   │   │       ├── event.py
│   │   │       └── calendar_requests.py
│   │   │
│   │   └── ai/                # AI module
│   │       ├── controllers/
│   │       │   └── ai_controller.py
│   │       ├── services/
│   │       │   ├── ai_service.py
│   │       │   └── openai_service.py
│   │       └── models/
│   │           ├── chat.py
│   │           └── ai_requests.py
│   │
│   ├── shared/                # Shared components
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── redis_connection.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base_exceptions.py
│   │   │   ├── auth_exceptions.py
│   │   │   ├── calendar_exceptions.py
│   │   │   └── ai_exceptions.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   ├── helpers.py
│   │   │   └── decorators.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth_middleware.py
│   │       ├── error_handler.py
│   │       └── logging_middleware.py
│   │
│   └── tests/                 # Test files
│       ├── conftest.py
│       └── modules/
│           ├── auth/
│           ├── calendar/
│           └── ai/
```

## Data Source
**Google Calendar as Single Source of Truth**
- No local database for calendar data
- All calendar operations go through Google Calendar API
- Optional Redis for temporary token storage and caching
- Server acts as a mediator/proxy

## Technology Stack
- **Backend**: FastAPI (Python 3.9+)
- **Package Management**: Poetry
- **External APIs**: Google Calendar API, OpenAI API
- **Caching**: Redis (optional)
- **Validation**: Pydantic
- **Authentication**: Google OAuth2 + JWT
- **HTTP Client**: httpx

## API Endpoints

### Authentication
- `POST /auth/google` - Google OAuth login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user info

### Calendar
- `GET /calendar/calendars` - List user calendars
- `GET /calendar/events` - List events
- `POST /calendar/events` - Create event
- `PUT /calendar/events/{event_id}` - Update event
- `DELETE /calendar/events/{event_id}` - Delete event
- `GET /calendar/events/{event_id}` - Get event details

### AI
- `POST /ai/chat` - Chat with AI
- `POST /ai/parse-request` - Parse natural language request

## Development Phases

### Phase 1: Basic Infrastructure ✅
- Poetry project setup
- Basic FastAPI application
- Project structure creation
- Configuration management

### Phase 2: Authentication Module
- Google OAuth2 integration
- JWT token management
- User session handling

### Phase 3: Calendar Module
- Google Calendar API integration
- CRUD operations for events
- Calendar management

### Phase 4: AI Module
- OpenAI API integration
- Natural language processing
- Calendar action parsing

### Phase 5: Integration & Testing
- Module integration
- Error handling
- Basic testing

### Phase 6: Production Ready
- Optimization
- Security enhancements
- Docker setup
- Documentation

## Benefits of This Architecture

1. **Clear Separation of Concerns**: Controllers handle HTTP, Services handle business logic
2. **Easy Testing**: Each layer can be tested independently
3. **Maintainability**: Changes in one layer don't affect others
4. **Scalability**: Easy to add new features or modify existing ones
5. **Clean Code**: Single responsibility principle
6. **No Database Complexity**: Google Calendar as source of truth simplifies data management
