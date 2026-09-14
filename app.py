from flask import Flask, jsonify
from flask import request
import psycopg2

app = Flask(__name__)


@app.route("/health")
def health():

    try:

        conn = psycopg2.connect(
            host="gistest.postgres.database.azure.com",
            port="5432",
            database="postgres",
            user="adminelvis",
            password="Evsleo333"
        )

        cur = conn.cursor()

        cur.execute("SELECT version();")

        version = cur.fetchone()[0]

        conn.close()

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "version": version
        })

    except Exception as ex:

        return jsonify({
            "status": "error",
            "message": str(ex)
        }), 500


@app.route("/query")
def query():

    sql = request.args.get("sql")

    try:

        conn = psycopg2.connect(
            host="gistest.postgres.database.azure.com",
            port="5432",
            database="postgres",
            user="adminelvis",
            password="Evsleo333"
        )

        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(sql)

        result = cur.fetchall()

        conn.close()

        return jsonify(result)

    except Exception as ex:

        return jsonify({
            "status": "error",
            "message": str(ex)
        }), 500
