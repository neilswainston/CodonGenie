#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
	eval "$(docker-machine env default)"
fi

docker build -t codongenie .
docker run --detach --publish=80:80 codongenie