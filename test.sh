#!/usr/bin/env bash

container=$(docker run -d --network=host --rm -it -ePOSTGRES_PASSWORD=postgres -ePGUSER=postgres -ePGPASSWORD=postgres postgres:14.1-alpine)

sleep 5

pytest -v -s "$@"

docker stop ${container}
