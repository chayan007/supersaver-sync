from datetime import datetime

from fastapi import FastAPI

from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from routes.dashboard_routes import dashboard_router
from routes.offering_routes import offering_router
from routes.profile_routes import profile_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(profile_router, prefix="/profile")
app.include_router(offering_router, prefix="/offerings")


@app.api_route("/{path_name:path}", methods=[
    "GET", "POST", "OPTIONS",
    "PATCH", "PUT", "DELETE"
])
async def catch_all(request: Request, path_name: str):
    return {
        "base_url": request.base_url,
        "available_routes": [
            {
                "path": route.path,
                "name": route.name
            }
            for route in request.app.routes
        ],
        "request_method": request.method,
        "path_name": path_name,
        "message": "Request Received",
        "time": datetime.now()
    }

handler = Mangum(app)
