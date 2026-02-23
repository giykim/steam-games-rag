# Steam Games RAG (Retrieval Augmentated Generation)

(These commands are tailored for `git bash`)

## Deployed Infrastructure

```
                        ┌─────────────────────────────────────────┐
                        │               Railway                   │
  ┌─────────┐           │  ┌─────────────────┐  ┌──────────────┐  │
  │  User   │──HTTPS───►│  │ FastAPI Backend │  │  PostgreSQL  │  │
  │ Browser │◄──────────│  │ (Python/Uvicorn)│◄►│  + pgvector  │  │
  └─────────┘           │  └────────┬────────┘  └──────────────┘  │
       │                │           │                             │
       │                └───────────┼─────────────────────────────┘
       │                            │
       │   ┌────────────────────────┼────────────────────────┐
       │   │         External APIs  │                        │
       │   │  ┌─────────────────┐   │   ┌──────────────────┐ │
       │   │  │   OpenAI API    │◄──┘   │  Anthropic API   │ │
       │   │  │ (embeddings)    │       │  (Claude Sonnet) │ │
       │   │  └─────────────────┘       └────────┬─────────┘ │
       │   └─────────────────────────────────────┼───────────┘
       │                                         │
       ▼                                         │
  ┌──────────┐                                   │
  │  Vercel  │◄──────────────────────────────────┘
  │ (Next.js)│   chat response
  └──────────┘


  ETL Pipeline (run locally, writes to Railway PostgreSQL)

  ┌─────────┐    ┌────────────┐    ┌─────────────────┐    ┌──────────────┐
  │ Kaggle  │───►│    CSV     │───►│   OpenAI API    │───►│  PostgreSQL  │
  │ Dataset │    │ (raw data) │    │ (text-embedding │    │  + pgvector  │
  └─────────┘    └────────────┘    │  -3-small)      │    └──────────────┘
                                   └─────────────────┘
```

### Request Flow

1. User sends a message from the **Vercel** frontend
2. **FastAPI** on Railway embeds the query via **OpenAI** (`text-embedding-3-small`)
3. Embedded query performs cosine similarity search against **PostgreSQL/pgvector**
4. Top matching game descriptions and stats are retrieved as context
5. Context + conversation history is sent to **Claude Sonnet** via **Anthropic API**
6. Response is streamed back to the user

## Steps to set up local development:

## Setup (Virtual Environment)

Create virtual environment:
```
python -m venv venv
```

Activate virtual environment:
```
# MacOS / Linux
source venv/bin/activate

# Windows
./venv/Scripts/activate
```

Install project packages into virtual environment:
```
pip install -r requirements.txt
```

## Data Ingestion Pipeline

Make sure docker is open.

Start docker container:
```
docker compose up -d
```

Initialize database schema in docker container:
```
docker exec -i steam-games-rag-db-1 psql -U postgres -d steam_games < db/schema.sql
```

Run data ingestion pipeline:
```
python -m pipelines.ingestion.run
```

### Stand up API endpoints

```
python -m uvicorn api.main:app --reload
```

Go to http://127.0.0.1:8000/docs to test API.

### Test frontend

```
cd frontend
```

```
npm run dev
```

### Production Deployment

Deploy backend to Railway (PostgreSQL Database and Backend Router).

Initialize psql database schema:
```
psql <public-database-url> < db/schema.sql
```

Deploy frontend to Vercel.

Set `NEXT_PUBLIC_API_URL` environment variable to Railway public url.

## Related Links

[Kaggle Dataset](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)