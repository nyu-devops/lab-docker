# Image for a Python 3 development environment
FROM quay.io/rofrano/nyu-devops-base:sp26

ARG USERNAME=vscode

# Set up the global Python development environment
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN python -m pip install -U pip pipenv && \
    pipenv install --system --dev

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

EXPOSE 8080

# Become a regular user for development
USER $USERNAME
