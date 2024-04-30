import boto3
import os
from dotenv import load_dotenv
from typing import Union
import logging
from fastapi import FastAPI, Request, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
import time

from getSignedUrl import getSignedUrl

load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


class Post(BaseModel):
    title: str
    body: str


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))


@app.post("/posts")
async def post_a_post(post: Post, authorization: str | None = Header(default=None)):

    logger.info(f"title : {post.title}")
    logger.info(f"body : {post.body}")
    logger.info(f"user : {authorization}")

    postId = f'POST#{uuid.uuid4()}'

    # Doit retourner le résultat de la requête la table dynamodb
    data = table.put_item(Item={"user": "USER#" + authorization, "post": postId, "body": post.body})
    return data


@app.get("/posts")
async def get_all_posts(user: Union[str, None] = None):

    if user is None:
        data = table.scan()
    else:
        data = table.query(KeyConditionExpression=Key("user").eq("USER#" + user))
    return data


@app.delete("/posts/{post_id}")
async def get_post_user_id(post_id: str):
    
    data = table.delete_item(
        Key={'post' : 'POST#'*(post_id[0] == 'P') + post_id,} # On sait pas trop si en argument il y a le POST# ou pas ducoup on filtre
    )
    return data


@app.get("/signedUrlPut")
async def get_signed_url_put(
    filename: str,
    filetype: str,
    postId: str,
    authorization: str | None = Header(default=None),
):
    return getSignedUrl(filename, filetype, postId, authorization)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
