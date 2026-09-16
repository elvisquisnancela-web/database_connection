from flask import Flask, jsonify
from flask import request
import psycopg2
from psycopg2.extras import RealDictCursor
import os

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

        cur= conn.cursor()
        geojson_sql = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(
                json_agg(
                    ST_AsGeoJSON(q.*)::json
                ),
                '[]'::json
            )
        )
        FROM (
            {sql}
        ) q
        """
        
        cur.execute(geojson_sql)
        
        result = cur.fetchone()[0]
        
        conn.close()
        
        return jsonify(result)

    except Exception as ex:

        return jsonify({
            "status": "error",
            "message": str(ex)
        }), 500
