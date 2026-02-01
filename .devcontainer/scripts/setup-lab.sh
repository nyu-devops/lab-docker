#!/bin/bash
echo "Setting up Docker lab environment..."
docker pull redis:6-alpine
docker pull python:3.12-slim
docker run --restart=always -d --name redis -p 6379:6379 -v redis:/data redis:6-alpine
echo "Setup complete"