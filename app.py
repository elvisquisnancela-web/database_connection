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
    if not sql:
        return jsonify({
            "status": "error",
            "message": "Missing SQL parameter"
        }), 400

    try:

        conn = psycopg2.connect(
            host="gistest.postgres.database.azure.com",
            port="5432",
            database="postgres",
            user="adminelvis",
            password="Evsleo333"
        )

        cur = conn.cursor()

        # =====================================================
        # DETECT GEOMETRY
        # =====================================================

        schema_sql = f"""
        SELECT *
        FROM (
            {sql}
        ) q
        LIMIT 0
        """

        cur.execute(schema_sql)
        
        columns = [desc.name.lower() for desc in cur.description]
        
        print("Columns:", columns)
        
        has_geom = "geom" in columns
        
        print("Has geometry:", has_geom)

        # =====================================================
        # SPATIAL QUERY -> GEOJSON
        # =====================================================

        if has_geom:

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

        # =====================================================
        # NON-SPATIAL QUERY -> TABLE JSON
        # =====================================================

        else:

            cur = conn.cursor(
                cursor_factory=RealDictCursor
            )

            cur.execute(sql)

            result = cur.fetchall()

            conn.close()

            return jsonify({
                "type": "table",
                "rows": rows
            })

    except Exception as ex:

        return jsonify({
            "status": "error",
            "message": str(ex)
        }), 500

