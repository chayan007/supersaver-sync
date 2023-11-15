from fastapi import FastAPI

from mangum import Mangum

from routes.dashboard_routes import dashboard_router
from routes.offering_routes import offering_router
from routes.profile_routes import profile_router

app = FastAPI()

app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(profile_router, prefix="/profile")
app.include_router(offering_router, prefix="/offerings")

handler = Mangum(app)
