import copy
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum


# app = FastAPI(openapi_url="/lambda-docker-fastapi-mangum/openapi.json", docs_url="/lambda-docker-fastapi-mangum/docs")
app = FastAPI(root_path="/stg/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    # res = requests.get("http://localhost:7000")
    # return {"Python": "success", "healthCheck": json.loads(res.content)}

    return "Hello from FastAPI"


@app.post("/")
def post_home():
    return "Hello from FastAPI from post_home"

@app.get("/health-check")
def health_check():
    return "OK"


def fix_missing_field(event):
    if "requestContext" not in event:
        event["requestContext"] = {}
    if "path" not in event:
        event["path"] = ""
    if "httpMethod" not in event:
        event["httpMethod"] = "GET"


def handler(event, context):
    print("<" * 100)
    print(json.dumps(event))

    fix_missing_field(event) 
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context) # Call the instance with the event arguments

    print("DONE")
    print(">" * 100)
    return response