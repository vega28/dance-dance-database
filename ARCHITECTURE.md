# Dance Dance Database - Architecture Diagram

## System Architecture

```mermaid
graph TB
    Client["Browser / React App<br/>(Vite)"]
    Flask["Flask API Server<br/>api/api.py"]
    DB["PostgreSQL Database<br/>dancenerd_development"]
    
    Client -->|HTTP Requests| Flask
    Flask -->|HTTP Responses| Client
    Flask -->|SQL Queries| DB
    DB -->|Query Results| Flask
    
    style Client fill:#61dafb,stroke:#333,stroke-width:2px,color:#000
    style Flask fill:#000,stroke:#333,stroke-width:2px,color:#fff
    style DB fill:#336791,stroke:#333,stroke-width:2px,color:#fff
```

## API Endpoints

```mermaid
graph LR
    Flask["Flask API"]
    
    Hello["/api/hello<br/>GET"]
    Artists["/api/artists<br/>GET"]
    Songs["/api/songs<br/>GET"]
    
    Flask --> Hello
    Flask --> Artists
    Flask --> Songs
    
    style Flask fill:#000,stroke:#333,stroke-width:2px,color:#fff
    style Hello fill:#90ee90,stroke:#333,stroke-width:1px
    style Artists fill:#87ceeb,stroke:#333,stroke-width:1px
    style Songs fill:#ffa07a,stroke:#333,stroke-width:1px
```

## Database Schema

```mermaid
graph TD
    Artists["<b>artists</b><br/>---<br/>id: int (PK)<br/>name: string (UNIQUE)<br/>"]
    Songs["<b>songs</b><br/>---<br/>id: int (PK)<br/>title: string<br/>artist_id: int (FK)<br/>status: string<br/>"]
    
    Artists -->|1:N| Songs
    
    style Artists fill:#b3e5fc,stroke:#333,stroke-width:2px
    style Songs fill:#ffe0b2,stroke:#333,stroke-width:2px
```

## Application Stack

| Layer | Technology | Location |
|-------|-----------|----------|
| **Frontend** | React + Vite | `src/` |
| **Backend** | Flask + SQLAlchemy | `api/api.py` |
| **Database** | PostgreSQL | `dancenerd_development` |
| **Migrations** | Flask-Migrate (Alembic) | `migrations/` |
| **Testing** | pytest | `tests/` |

## Request Flow Example: Get All Songs

```mermaid
sequenceDiagram
    participant Browser as Browser/React
    participant Flask as Flask API
    participant DB as PostgreSQL
    
    Browser->>Flask: GET /api/songs
    Flask->>Flask: Route handler: get_songs()
    Flask->>DB: SELECT * FROM songs
    DB-->>Flask: Song rows + artist_ids
    Flask->>DB: (Lazy load artists via FK)
    Flask->>Browser: JSON response: songs
    Browser-->>Browser: Render in UI
```

## Current Status

✅ **Implemented:**
- PostgreSQL database with Artist and Song models
- Flask API with basic demo routes
- Flask-Migrate for schema versioning
- pytest with fixtures for integration and unit tests
- Database seeding via `flask seed` command

⏳ **Not Yet Implemented:**
- Frontend React components
- CRUD endpoints
- Authentication/Authorization
- Input validation
- Error handling
- API documentation (Swagger/OpenAPI)
