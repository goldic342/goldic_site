from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from index.router import router
from blog.router import router as blog_router
from admin.router import router as admin_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(blog_router)
app.include_router(admin_router)
