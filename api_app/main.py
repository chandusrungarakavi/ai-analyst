from fastapi import FastAPI, HTTPException
import psycopg2
import os

app = FastAPI()


# Database connection settings from environment variables
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    return conn


@app.get("/fetch")
def fetch_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 AS result"
        )  # Example query, replace with your table/query
        row = cur.fetchone()
        cur.close()
        conn.close()
        return {"result": row[0] if row else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
