from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from index.router import router
from blog.router import router as blog_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(blog_router)
