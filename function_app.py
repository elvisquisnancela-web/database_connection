import azure.functions as func
import psycopg2

app = func.FunctionApp()

# =====================================================
# HEALTH CHECK
# =====================================================

@app.route(
    route="health",
    auth_level=func.AuthLevel.ANONYMOUS
)
def health(req: func.HttpRequest):

    return func.HttpResponse(
        "OK",
        status_code=200
    )


# =====================================================
# DATABASE TEST
# =====================================================

@app.route(
    route="dbtest",
    auth_level=func.AuthLevel.ANONYMOUS
)
def dbtest(req: func.HttpRequest):

    try:

        conn = psycopg2.connect(
            host="gistest.postgres.database.azure.com",
            database="postgres",
            user="adminelvis",
            password="Evsleo333",
            port=5432,
            sslmode="require"
        )

        cur = conn.cursor()

        cur.execute("""
            SELECT
                current_database(),
                current_user,
                version();
        """)

        row = cur.fetchone()

        cur.close()
        conn.close()

        return func.HttpResponse(
            str({
                "database": row[0],
                "user": row[1]
            }),
            status_code=200
        )

    except Exception as e:

        return func.HttpResponse(
            str(e),
            status_code=500
        )
