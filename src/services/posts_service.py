from src.database import psycopg

cursor = psycopg.cursor

def get_all():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

def get_latest():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;""")
    posts = cursor.fetchall()
    return posts

def get_byid(post_id: int):
    cursor.execute("""SELECT * from posts WHERE post_id = %s """, (str(post_id),))
    posts = cursor.fetchone()
    return posts