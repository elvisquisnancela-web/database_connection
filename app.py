from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

# =====================================================
# ROOT
# =====================================================

@app.route("/")
def home():
    return {
        "application": "GIS Lab",
        "status": "running"
    }


# =====================================================
# HEALTH
# =====================================================

@app.route("/health")
def health():

    db_status = "not configured"

    try:

        db_host = os.getenv("DB_HOST")

        if db_host:

            conn = psycopg2.connect(
                host="gistest.postgres.database.azure.com",
                port="DB_PORT","5432",
                database="postgres",
                user="adminelvis",
                password="Evsleo333"
            )

            conn.close()

            db_status = "connected"

    except Exception as e:

        db_status = str(e)

    return jsonify({
        "status": "healthy",
        "database": db_status
    })


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80
    )
