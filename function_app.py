import azure.functions as func
import psycopg2

app = func.FunctionApp()

@app.route(
    route="health",
    auth_level=func.AuthLevel.ANONYMOUS
)
def health(req: func.HttpRequest):

    return func.HttpResponse(
        "OK",
        status_code=200
    )



