from src.database import psycopg

cursor = psycopg.cursor
conn = psycopg.conn

def user_post(post):
    print(post)
    cursor.execute("""INSERT INTO posts (title, content, subreddit, user) VALUES (%s, %s, %s, %s) RETURNING * """,
                    (post.title, post.content, post.subreddit, post.user, ))
    new_post = cursor.fetchone()

    conn.commit()

    return new_post