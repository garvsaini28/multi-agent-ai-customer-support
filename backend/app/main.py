from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router
from app.database.connection import get_database


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered customer support system using Multi-Agent Architecture",
    version=settings.APP_VERSION
)


# ==============================
# CORS CONFIGURATION
# ==============================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==============================
# API ROUTES
# ==============================

app.include_router(
    router,
    prefix=settings.API_PREFIX,
    tags=["Chat"]
)


# ==============================
# HOME ROUTE
# ==============================

@app.get("/")
def home():

    try:

        # Test MongoDB Connection
        db = get_database()

        db.command("ping")


        return {

            "status": "success",

            "message": "Backend is running successfully 🚀",

            "database": "Connected ✅"

        }


    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }