#!/usr/bin/env bash
docker build -t codongenie .
docker run -d -p $1:5000 codongenie