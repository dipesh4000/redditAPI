from src.database import psycopg
from fastapi import HTTPException, status
from typing import List
from src.pydantic_models.posts_models import Post, PostFull

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
        conn.commit()
        return new_post
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    
def update_post(id:int, updated_value: Post) -> PostFull:
    post = get_post_by_id(id)

    for key, value in updated_value:
        post[key] = updated_value[value]
        

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                    (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    return updated_post


def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    return deleted_post