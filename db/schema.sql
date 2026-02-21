CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS description_embeddings_openai (
    id SERIAL PRIMARY KEY,
    app_id INTEGER UNIQUE,
    name TEXT,
    content TEXT,
    embedding vector(1536)
);

CREATE TABLE IF NOT EXISTS stats_embeddings_openai (
    id SERIAL PRIMARY KEY,
    app_id INTEGER UNIQUE,
    name TEXT,
    content TEXT,
    embedding vector(1536)
);

CREATE TABLE IF NOT EXISTS description_embeddings_st (
    id SERIAL PRIMARY KEY,
    app_id INTEGER UNIQUE,
    name TEXT,
    content TEXT,
    embedding vector(384)
);

CREATE TABLE IF NOT EXISTS stats_embeddings_st (
    id SERIAL PRIMARY KEY,
    app_id INTEGER UNIQUE,
    name TEXT,
    content TEXT,
    embedding vector(384)
);
