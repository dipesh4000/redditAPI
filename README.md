# redditAPI

A Reddit-like REST API built with FastAPI and PostgreSQL.

## Features

- Browse and search posts by subreddit or ID
- Create, update, and delete posts
- User signup and login with JWT authentication
- Password hashing with Argon2
- Protected routes — only the post owner can update or delete their posts

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** + **psycopg2** — database
- **python-jose** — JWT tokens
- **passlib[argon2]** — password hashing
- **pydantic** — request/response validation
- **uvicorn** — ASGI server

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file:
   ```
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

## Authentication

Protected routes require a Bearer token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```
Obtain the token from `POST /login`.

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|:---:|-------------|
| GET | `/` | No | Get all posts |
| POST | `/signup` | No | Register a new user |
| POST | `/login` | No | Login and receive JWT token |
| GET | `/r/latest` | No | Get 10 latest posts |
| GET | `/r/{post_id}` | No | Get post by ID |
| GET | `/u/{username}` | No | Get all posts by a user |
| POST | `/u/post` | Yes | Create a post |
| PUT | `/u/update/{post_id}` | Yes | Update a post (owner only) |
| DELETE | `/u/delete/{post_id}` | Yes | Delete a post (owner only) |

> `PUT` and `DELETE` return `403 Forbidden` if the authenticated user is not the post owner.

Interactive docs available at `/docs` after running the server.
