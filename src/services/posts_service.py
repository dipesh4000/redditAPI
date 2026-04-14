from src.database import psycopg
from fastapi import HTTPException, status
from typing import List
from src.pydantic_models.posts_models import Post, PostFull, PostUpdate

cursor = psycopg.cursor
conn = psycopg.conn

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
        cursor.execute("""SELECT * from posts WHERE post_id = %s """, (post_id,))
        posts = cursor.fetchone()
        if posts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return posts
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

def create_post(post: Post, current_user) -> PostFull:
    try:
        cursor.execute("""INSERT INTO posts (title, content, subreddit, "user") VALUES (%s, %s, %s, %s) RETURNING * """,
                       (post.title, post.content, post.subreddit, current_user["username"]))
        new_post = cursor.fetchone()
        conn.commit()
        return new_post
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    
def update_post(post_id: int, updated_value: PostUpdate, current_user) -> Post:
    try:
        existing_post = dict(get_byid(post_id))

        if existing_post["user"] != current_user["username"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

        updates = updated_value.model_dump(exclude_none=True)
        existing_post.update(updates)

        cursor.execute(
            """UPDATE posts SET title = %s, content = %s, subreddit = %s, "user" = %s WHERE post_id = %s RETURNING *""",
            (existing_post["title"], existing_post["content"], existing_post["subreddit"], existing_post["user"], post_id)
        )
        updated_post = cursor.fetchone()
        conn.commit()
        return updated_post
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")


def delete_post(post_id: int, current_user):
    try:
        existing_post = dict(get_byid(post_id))

        if existing_post["user"] != current_user["username"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

        cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""", (post_id,))
        deleted_post = cursor.fetchone()
        conn.commit()
        return deleted_post
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")