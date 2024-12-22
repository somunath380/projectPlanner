from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router
from routes.team import teams_router
from routes.project import projects_router

load_dotenv()

# from db import connection
# app = FastAPI(lifespan=connection.lifespan)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/api/v1")
app.include_router(teams_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
