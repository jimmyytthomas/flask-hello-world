from flask import Flask
import os 
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def hello_world():
    return 'Hello, World from Jimmy Thomas in 3308!'


@app.route('/db_test')
def db_test():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route('/db_create')
def db_create():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Basketball (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            team VARCHAR(100),
            position VARCHAR(50)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    return "Basketball table created successfully!"


@app.route('/db_insert')
def db_insert():
    conn = get_db_connection()
    cur = conn.cursor()

    players = [
        ("Jayson Tatum", "Boston Celtics", "Forward"),
        ("Stephen Curry", "Golden State Warriors", "Guard"),
        ("Nikola Jokic", "Denver Nuggets", "Center"),
        ("Jimmy Thomas", "CU Boulder", "Forward")
    ]

    cur.executemany(
        "INSERT INTO Basketball (name, team, position) VALUES (%s, %s, %s);",
        players
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Basketball data inserted successfully!"


@app.route('/db_select')
def db_select():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Basketball;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    output = ""

    for row in rows:
        output += f"{row}<br>"

    return output

