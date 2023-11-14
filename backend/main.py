from typing import Union

from fastapi import FastAPI

from routes.profile_routes import profile_router

app = FastAPI()

app.include_router(profile_router, prefix="/profile")
