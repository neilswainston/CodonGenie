#!/usr/bin/env bash
docker build -t codongenie .
docker run -d -p 80:80 codongenie