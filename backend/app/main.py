from fastapi import FastAPI

app = FastAPI(
    title="Multi-Agent AI Customer Support",
    description="AI-powered customer support system using Multi-Agent Architecture",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Backend is running successfully 🚀"
    }