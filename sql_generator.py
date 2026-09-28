from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="1U6l7PDeL8nUJD2HJvYlhIEIEzGhoICorr6UOU90zLaFABDcdfMgJQQJ99CHACR0EKYXJ3w3AAAAACOGwp9Z",
    api_version="2024-10-21",
    azure_endpoint="https://fundry-gis.services.ai.azure.com"
)


SCHEMA_DESCRIPTION = """
Available layers:

vw_pole_count_subarea(
    subarea,
    pole_count
)

neo_subarea(
    subarea,
    geom
)

poles(
    geom
)

municipalities(
    name_def,
    geom
    )

PostGIS functions:

ST_Within(point_geom, polygon_geom)

"""


def generate_sql(question):

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": f"""
You generate PostgreSQL SQL.

{SCHEMA_DESCRIPTION}

Rules:

1. Generate only SELECT statements.
2. Return SQL only.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content.strip()


def generate_answer(question, rows):

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": """
You are a GIS assistant.

Answer the user's question using the database result.

Be concise and clear.
"""
            },
            {
                "role": "user",
                "content": f"""
Question:

{question}

Database result:

{rows}
"""
            }
        ]
    )

    return response.choices[0].message.content.strip()
