import azure.functions as func
import importlib.util

app = func.FunctionApp()

@app.route(
    route="packages",
    auth_level=func.AuthLevel.ANONYMOUS
)
def packages(req: func.HttpRequest):

    return func.HttpResponse(
        str({
            "psycopg2": importlib.util.find_spec("psycopg2") is not None,
            "psycopg": importlib.util.find_spec("psycopg") is not None
        })
    )
