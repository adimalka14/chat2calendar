# Chat2Calendar Server

AI-powered Google Calendar integration server built with FastAPI and Python.

## Features

- **Google OAuth2 Authentication** - Secure login with Google accounts
- **Google Calendar Integration** - Full CRUD operations for calendar events
- **AI-Powered Assistance** - Natural language processing for calendar operations
- **Modular Architecture** - Clean separation of concerns with Controller-Service pattern
- **RESTful API** - Well-documented API endpoints

## Architecture

This project follows a modular monolithic architecture with clear separation between:

- **Controllers** - Handle HTTP requests/responses and validation
- **Services** - Implement business logic and external API integration
- **Models** - Define data structures and validation schemas
- **Shared** - Common utilities, exceptions, and middleware

## Technology Stack

- **Backend**: FastAPI (Python 3.9+)
- **Package Management**: Poetry
- **External APIs**: Google Calendar API, OpenAI API
- **Caching**: Redis (optional)
- **Validation**: Pydantic
- **Authentication**: Google OAuth2 + JWT

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry
- Google Cloud Project with Calendar API enabled
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chat2calendar/server
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the server**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

The server will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file with the following variables:

```env
# Server Configuration
APP_NAME=Chat2Calendar Server
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth2
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Google Calendar API
GOOGLE_CALENDAR_SCOPES=https://www.googleapis.com/auth/calendar

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Redis (Optional)
REDIS_URL=redis://localhost:6379

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

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

## Development

### Project Structure

```
server/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration
│   ├── dependencies.py        # FastAPI dependencies
│   ├── modules/               # Feature modules
│   │   ├── auth/              # Authentication
│   │   ├── calendar/          # Calendar operations
│   │   └── ai/                # AI integration
│   ├── shared/                # Shared components
│   │   ├── database/          # Database connections
│   │   ├── exceptions/        # Custom exceptions
│   │   ├── utils/             # Utility functions
│   │   └── middleware/        # Custom middleware
│   └── tests/                 # Test files
├── pyproject.toml             # Poetry configuration
├── env.example               # Environment variables template
└── README.md
```

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black .
poetry run isort .
```

### Type Checking

```bash
poetry run mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
