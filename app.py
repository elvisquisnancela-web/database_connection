import azure.functions as func
import psycopg2
import os

app = func.FunctionApp()

@app.route(
    route="dbtest",
    auth_level=func.AuthLevel.ANONYMOUS
)
def dbtest(req: func.HttpRequest):

    try:

        conn = psycopg2.connect(
            host=os.environ["gistest.postgres.database.azure.com"],
            database=os.environ["postgres"],
            user=os.environ["adminelvis"],
            password=os.environ["Evsleo333"],
            sslmode="require"
        )

        cur = conn.cursor()

        cur.execute("SELECT current_database();")

        db = cur.fetchone()[0]

        cur.close()
        conn.close()

        return func.HttpResponse(
            f"Connected to {db}",
            status_code=200
        )

    except Exception as e:

        return func.HttpResponse(
            str(e),
            status_code=500
        )

