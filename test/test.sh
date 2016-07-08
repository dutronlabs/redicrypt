#!/usr/bin/env bash
if [ $1 = "-kill" ]; then
    docker rm -f redis-server-def redis-server-dyn redis-server-fx redis-server-pw
else
    docker run -d --name redis-server-def -p 6379:6379 redis
    docker run -d --name redis-server-dyn -p 32769:6379 redis
    docker run -d --name redis-server-fx -p 9999:6379 redis
    docker run -d --name redis-server-pw -p 6380:6379 redis redis-server --requirepass password
#python -m unittest discover
fi