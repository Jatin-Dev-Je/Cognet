# Backend

Cognet's backend is the execution and intelligence layer that serves the application, stores memory, and coordinates retrieval and reasoning.

## Structure

```text
backend/
|
├── app/                        # Main application
├── tests/                      # Tests
├── scripts/                    # Utility scripts (DB seed, etc.)
├── docs/                       # Backend docs
|
├── .env
├── .env.example
├── requirements.txt
├── pyproject.toml
├── README.md
```

## Purpose

### app/

Contains the FastAPI application, API routes, service layers, configuration, and core domain logic.

### tests/

Contains backend test coverage for APIs, services, and data access behavior.

### scripts/

Contains operational scripts such as database seeding, migration helpers, and maintenance utilities.

### docs/

Contains backend-specific documentation, design notes, and implementation references.

## Configuration Files

### .env

Local environment variables for development.

### .env.example

Template for required environment variables.

### requirements.txt

Python dependencies for the backend.

### pyproject.toml

Project metadata, tooling configuration, and packaging settings.

### README.md

Backend-specific documentation and setup guidance.

## Backend Responsibilities

The backend is responsible for:

* serving the API surface for Cognet
* connecting to MongoDB and vector storage
* orchestrating memory ingestion and retrieval
* integrating with AI services such as OpenAI
* exposing internal services to the interface layer

## Notes

This folder is intended to evolve into the main Python service for the Cognet system.