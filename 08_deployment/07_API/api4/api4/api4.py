import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

class BlogArticles(BaseModel):
    title: str
    content: str
    author: str = "Anonymous Author"

@app.get("/")
async def index():

    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message

@app.post("/create-blog-article")
async def create_blog_article(blog_article: BlogArticles):
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/articles.csv")
    new_article = pd.Series({
        'id': len(df)+1,
        'title': blog_article.title,
        'content': blog_article.content,
        'author': blog_article.author
    })

    df = df.append(new_article, ignore_index=True)

    return df.tail(1).to_json()

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)