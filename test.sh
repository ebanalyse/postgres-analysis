#!/usr/bin/env bash

container=$(docker run -d --rm -it -e POSTGRES_PASSWORD=postgres -e PGUSER=postgres -e PGPASSWORD=postgres -p 5432:5432 postgres:14.1-alpine)

sleep 5

pytest -v -s "$@"

docker stop ${container}