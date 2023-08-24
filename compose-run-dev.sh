#! /usr/bin/env bash

# start docker compose with dev configuration
docker compose -f docker-compose.yml -f docker-compose.dev.yml up