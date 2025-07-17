from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from routes import auth, dashboard, package, survey, data, api
from db import Base, engine
from init_db import init_database

# בתחילת main.py
init_database()



app = FastAPI(title="Game Metrics")

# ✅ Mount static files **right after app creation**
app.mount("/static", StaticFiles(directory="static"), name="static")

# Middleware
app.add_middleware(SessionMiddleware, secret_key="BvJ1yGrpN7uTOzA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB init
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(package.router)
app.include_router(survey.router)
app.include_router(data.router)
app.include_router(api.router) 
