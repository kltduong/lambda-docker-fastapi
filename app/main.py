import json

import numpy as np

from typing import List
from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .embeddings import get_embeddings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextGroup(BaseModel):
    texts: List[str]


@app.get("/")
def home():
    return "Hello from FastAPI"


@app.post("/embeddings")
def handle_embeddings(text_group: TextGroup):
    embeddings = get_embeddings(text_group.texts)
    embedding1 = embeddings[0] / np.linalg.norm(embeddings[0])
    embedding2 = embeddings[1] / np.linalg.norm(embeddings[1])
    similarity = np.dot(embedding1, embedding2)

    res = {"similarity": str(similarity)}

    return res


@app.get("/health-check")
def health_check():
    return "OK"


def fix_missing_fields(event):
    if "requestContext" not in event:
        event["requestContext"] = {}
    if "path" not in event:
        event["path"] = ""
    if "httpMethod" not in event:
        event["httpMethod"] = "GET"


def handler(event, context):
    print("<" * 100)
    print(json.dumps(event))

    fix_missing_fields(event)
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)  # Call the instance with the event arguments

    print("DONE")
    print(">" * 100)
    return response
