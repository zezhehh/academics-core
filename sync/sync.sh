#!/bin/bash

source .env

# Sync local database with vercel postgresql
PG_PASSWORD=$POSTGRES_PASSWORD pg_dump $POSTGRES_DATABASE > pg.bkp.vercel -h $POSTGRES_HOST -U $POSTGRES_USER
PG_PASSWORD=postgres psql -h $POSTGRES_HOST -U default -c "DROP DATABASE $POSTGRES_DATABASE"
PG_PASSWORD=postgres psql -h $POSTGRES_HOST -U default -c "CREATE DATABASE $POSTGRES_DATABASE"
PG_PASSWORD=postgres psql academics -h $POSTGRES_HOST -U default < pg.bkp.vercel

# Dump local database to json and sync with meilisearch
rm institutions.json
go run main.go
