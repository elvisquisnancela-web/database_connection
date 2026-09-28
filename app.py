from flask import Flask, jsonify
from flask import request
from flask import render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import AzureOpenAI
import os

from sql_generator import generate_sql
from sql_generator import generate_answer


app = Flask(__name__)

DB_CONFIG = {
    "host": "gistest.postgres.database.azure.com",
    "database": "postgres",
    "user": "adminelvis",
    "password": "Evsleo333"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)




@app.route("/hello")
def hello():
    return "<h1>Hello, my friend!</h1>"



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

            rows = cur.fetchall()

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




@app.route("/query2")
def query2():

    question = request.args.get("question")

    if not question:
        return jsonify({
            "error": "Question parameter missing"
        }), 400

    sql = generate_sql(question)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)

    rows = cur.fetchall()

    conn.close()

    answer = generate_answer(
    question,
    rows
    )

    return jsonify({
        "question": question,
        "answer": answer,
        "generated_sql": sql,
        "rows": rows
    })



@app.route("/abc123")
def abc123():
    return render_template("chat.html")



@app.route("/routes")
def routes():
    return "\n".join(str(r) for r in app.url_map.iter_rules())


if __name__ == "__main__":
    app.run(debug=True)




