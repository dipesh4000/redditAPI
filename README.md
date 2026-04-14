# redditAPI

A Reddit-like REST API built with FastAPI and PostgreSQL.

## Overview

This project provides a simple API for posts and users, including signup/login, JWT authentication, and owner-protected post updates and deletes. The backend uses raw SQL with `psycopg2` and a connection pool.

## Features

- Create and retrieve posts
- List latest posts
- List posts by username
- Create, update, and delete posts as an authenticated user
- User signup and login with JWT tokens
- Password hashing with Argon2
- Owner-only authorization for post edits/deletes

## Project Structure

- `src/main.py` — app initialization, CORS setup, router registration, root endpoints
- `src/config.py` — environment-backed settings with `pydantic-settings`
- `src/database/psycopg.py` — PostgreSQL connection pool
- `src/routes/posts/posts.py` — post-related public endpoints
- `src/routes/user/user.py` — user-related and authenticated post endpoints
- `src/schemas/posts_models.py` — Pydantic models for post requests/responses
- `src/schemas/users_models.py` — Pydantic models for user auth and tokens
- `src/services/authservice.py` — user registration and login logic
- `src/services/posts_service.py` — database operations for posts
- `src/services/user_service.py` — JWT creation and bearer auth dependency

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** + **psycopg2** — database access
- **PyJWT** — JWT token creation and verification
- **passlib[argon2]** — password hashing
- **pydantic** / **pydantic-settings** — validation and environment loading
- **uvicorn** — development server

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=<your_secret_key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_HOSTNAME=<your_db_host>
   DATABASE_NAME=<your_db_name>
   DATABASE_USERNAME=<your_db_user>
   DATABASE_PASSWORD=<your_db_password>
   DATABASE_PORT=<your_db_port>
   ```

3. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|:---:|---|
| GET | `/health` | No | Health check |
| GET | `/` | No | Get all posts |
| POST | `/signup` | No | Register a new user |
| POST | `/login` | No | Login and receive JWT token |
| GET | `/posts/` | No | Get all posts |
| GET | `/posts/latest` | No | Get latest posts |
| GET | `/posts/{post_id}` | No | Get a post by ID |
| GET | `/users/{username}/posts` | No | Get posts by username |
| POST | `/users/posts` | Yes | Create a new post |
| PUT | `/users/posts/{post_id}` | Yes | Update a post (owner only) |
| DELETE | `/users/posts/{post_id}` | Yes | Delete a post (owner only) |

## Authentication

Protected routes require a Bearer token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

Obtain the token by logging in via `POST /login`.

## Notes

- The app currently uses open CORS (`*`) for development.
- `src/database/session.py` and `src/models/models.py` are present as placeholders and are not used by the current SQL-based implementation.
- Interactive API docs are available at `/docs` once the server is running.
