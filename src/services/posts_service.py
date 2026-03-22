from src.database import psycopg
from fastapi import HTTPException, status
from typing import List
from src.pydantic_models.posts_models import Post, PostFull

cursor = psycopg.cursor

def get_all() -> List[Post]:
    try:
        cursor.execute("""SELECT * FROM posts """)
        posts = cursor.fetchall()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

def get_latest() -> List[Post]:
    try:
        cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;""")
        posts = cursor.fetchall()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

def get_byid(post_id: int) -> PostFull:
    try:
        cursor.execute("""SELECT * from posts WHERE post_id = %s """, (str(post_id),))
        posts = cursor.fetchone()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

def create_post(post: Post) -> PostFull:
    try:
        cursor.execute("""INSERT INTO posts (title, content, subreddit, "user") VALUES (%s, %s, %s, %s) RETURNING * """,
                       (post.title, post.content, post.subreddit, post.user))
        new_post = cursor.fetchone()
        psycopg.conn.commit()
        return new_post
    except Exception as e:
        psycopg.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")