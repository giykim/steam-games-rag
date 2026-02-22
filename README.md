# Steam Games RAG (Retrieval Augmentated Generation)

(These commands are tailored for `git bash`)

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

## Related Links

[Kaggle Dataset](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)