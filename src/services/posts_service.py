from src.database import psycopg
import json

cursor = psycopg.cursor

def get_all():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

def get_latest():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

def get_byid(post_id: int):
    cursor.execute(f'"""SELECT * FROM posts WHERE post_id = {post_id}"""')
    posts = cursor.fetchall()
    return posts