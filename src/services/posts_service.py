from src.database import psycopg
from fastapi import HTTPException, status
from typing import List
from src.schemas.posts_models import Post, PostFull, PostUpdate


def get_all(limit: int = 20, offset: int = 0) -> List[PostFull]:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT post_id, title, content, subreddit, created_at, "user" FROM posts LIMIT %s OFFSET %s',
                (limit, offset),
            )
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def get_latest(limit: int = 10, offset: int = 0) -> List[PostFull]:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT post_id, title, content, subreddit, created_at, "user" FROM posts ORDER BY created_at DESC LIMIT %s OFFSET %s',
                (limit, offset),
            )
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def get_byid(post_id: int) -> PostFull:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT post_id, title, content, subreddit, created_at, "user" FROM posts WHERE post_id = %s',
                (post_id,),
            )
            post = cursor.fetchone()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def get_by_username(username: str) -> List[PostFull]:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT post_id, title, content, subreddit, created_at, "user" FROM posts WHERE "user" = %s ORDER BY created_at DESC',
                (username,),
            )
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def create_post(post: Post, current_user) -> PostFull:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO posts (title, content, subreddit, "user") VALUES (%s, %s, %s, %s) RETURNING post_id, title, content, subreddit, created_at, "user"',
                (post.title, post.content, post.subreddit, current_user["username"]),
            )
            new_post = cursor.fetchone()
        conn.commit()
        return new_post
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def update_post(post_id: int, updated_value: PostUpdate, current_user) -> PostFull:
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT post_id, title, content, subreddit, created_at, "user" FROM posts WHERE post_id = %s',
                (post_id,),
            )
            existing_post = cursor.fetchone()

            if existing_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            if existing_post["user"] != current_user["username"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

            update_data = updated_value.model_dump(exclude_none=True)
            title = update_data.get("title", existing_post["title"])
            content = update_data.get("content", existing_post["content"])
            subreddit = update_data.get("subreddit", existing_post["subreddit"])

            cursor.execute(
                'UPDATE posts SET title = %s, content = %s, subreddit = %s WHERE post_id = %s RETURNING post_id, title, content, subreddit, created_at, "user"',
                (title, content, subreddit, post_id),
            )
            updated_post = cursor.fetchone()
        conn.commit()
        return updated_post
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def delete_post(post_id: int, current_user):
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT post_id, "user" FROM posts WHERE post_id = %s', (post_id,))
            existing_post = cursor.fetchone()

            if existing_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            if existing_post["user"] != current_user["username"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

            cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        conn.commit()
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)
