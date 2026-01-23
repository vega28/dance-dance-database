# Dance Dance Database - Architecture Diagram

## System Architecture
<!-- FIXME: update and fix colors! -->

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
    %% Global Styles
    classDef get fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef post fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef put fill:#fff4dd,stroke:#d4a017,stroke-width:1px
    classDef delete fill:#ffebee,stroke:#c62828,stroke-width:2px

    Flask["🚀 Flask API"]
    style Flask fill:#000,color:#fff,stroke-width:2px

    %% General Section
    Flask --> Hello["/api/hello<br/>GET"]:::get

    %% Artist Section
    subgraph Artist_Resource [Artist Endpoints]
        direction LR
        A_Path["/api/artists"]
        A_ID_Path["/api/artists/&lt;id&gt;"]

        A_Path --> A_GET["GET (List)"]:::get
        A_Path --> A_POST["POST (Create)"]:::post

        A_ID_Path --> A_GET_ID["GET (Read)"]:::get
        A_ID_Path --> A_PUT["PUT (Update)"]:::put
        A_ID_Path --> A_DEL["DELETE (Delete)"]:::delete
    end

    %% Song Section
    subgraph Song_Resource [Song Endpoints]
        direction LR
        S_Path["/api/songs"]
        S_ID_Path["/api/songs/&lt;id&gt;"]

        S_Path --> S_GET["GET (List)"]:::get
        S_Path --> S_POST["POST (Create)"]:::post

        S_ID_Path --> S_GET_ID["GET (Read)"]:::get
        S_Path --> S_PUT["PUT (Update)"]:::put
        S_ID_Path --> S_DEL["DELETE (Delete)"]:::delete
    end

    

    %% Dance Section
    subgraph Dance_Resource [Dance Endpoints]
        direction LR
        D_Path["/api/dances"]
        D_ID_Path["/api/dances/&lt;id&gt;"]

        D_Path --> D_GET["GET (List)"]:::get
        D_Path --> D_POST["POST (Create)"]:::post

        D_ID_Path --> D_GET_ID["GET (Read)"]:::get
        D_ID_Path --> D_PUT["PUT (Update)"]:::put
        D_ID_Path --> D_DEL["DELETE (Delete)"]:::delete
    end

    Flask --> A_Path
    Flask --> A_ID_Path
    Flask --> S_Path
    Flask --> S_ID_Path
    Flask --> D_Path
    Flask --> D_ID_Path

```


## Database Schema

```mermaid
graph TD
    Artists["<b>artists</b><br/>---<br/>id: int (PK)<br/>name: string (UNIQUE)<br/>"]
    Songs["<b>songs</b><br/>---<br/>id: int (PK)<br/>title: string<br/>artist_id: int (FK)<br/>"]
    Dances["<b>dances</b><br/>---<br/>id: int (PK)<br/>status: enum<br/>song_id: int (FK)<br/>"]
    
    Artists -->|1:N| Songs
    Songs -->|1:1| Dances
    
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
- CRUD endpoints

⏳ **Not Yet Implemented:**
- Frontend React components
- Users and Login
- Authentication/Authorization
- Input validation
- Error handling
- API documentation (Swagger/OpenAPI)
