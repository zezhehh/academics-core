# !/bin/bash

source .env

docker run -d \
  --name postgres_15 \
  -p 5432:5432 \
  -e POSTGRES_USER=${DB_USER} \
  -e POSTGRES_PASSWORD=${DB_PWD} \
  -e POSTGRES_DB=academics \
  postgres:15
