import os
import psycopg2
from psycopg2.extras import DictCursor

def fetch_connection():
    # initialize DB (consider pooling)
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USERNAME']
    db_pass = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(host=db_host, database="postgres", user=db_user, password=db_pass, cursor_factory=DictCursor)

    return conn