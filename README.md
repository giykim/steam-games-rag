# Steam Games RAG (Retrieval Augmentated Generation)

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

Run data ingestion pipeline:
```
python -m pipelines.ingestion.run
```

## Related Links

[Kaggle Dataset](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)