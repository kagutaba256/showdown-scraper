#!/bin/bash
docker-compose -f /home/sam/serv/pokemon/ps-downloader/docker-compose.yml down
exec /home/sam/serv/pokemon/ps-downloader/run.sh
