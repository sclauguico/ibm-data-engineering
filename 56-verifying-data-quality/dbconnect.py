import os
import psycopg2
pgpassword = "2g507mzE3Mr0aMurG2LmCFB3"
conn = None
try:
    conn = psycopg2.connect(
        user = "postgres",
        password = pgpassword,
        host = "postgres",
        port = "5432",
        database = "postgres")
except Exception as e:
    print("Error connecting to data warehouse")
    print(e)
else:
    print("Successfully connected to warehouse")
finally:
    if conn:
        conn.close()
        print("Connection closed")