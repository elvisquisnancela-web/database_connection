from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# =====================================================
# DATABASE CONFIG
# =====================================================

DB_HOST = os.environ.get("gistest.postgres.database.azure.com")
DB_NAME = os.environ.get("postgres")
DB_USER = os.environ.get("adminelvis")
DB_PASSWORD = os.environ.get("Evsleo333")

# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():
    return {
        "status": "running",
        "service": "GeoAI Test App"
    }

# =====================================================
# DATABASE TEST
# =====================================================

@app.route("/dbtest")
def dbtest():

    try:

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode="require"
        )

        cur = conn.cursor()

        cur.execute("SELECT version();")

        version = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "status": "connected",
            "postgres": version
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    app.run()
