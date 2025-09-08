from fastapi import FastAPI
from routes.user_routes import user_router

# creates FastAPI application with user_router which has full path as src.routes.user_routes.py 
app = FastAPI()
app.include_router(user_router)
