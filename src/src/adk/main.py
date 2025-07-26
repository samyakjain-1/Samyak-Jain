from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session

from ..database import database
from .orchestrator import run_analysis

# Create DB tables
database.init_db()

app = FastAPI(
    title="MarketAI API",
    description="API for running financial hypothesis analysis with an agentic system.",
    version="0.1.0",
)

class HealthCheck(BaseModel):
    status: str

class HypothesisRequest(BaseModel):
    hypothesis: str
    mode: str = "analyze"

@app.get("/health", response_model=HealthCheck)
def health_check():
    """Endpoint to check if the API is running."""
    return {"status": "ok"}

@app.post("/process")
async def process_hypothesis(request: HypothesisRequest, db: Session = Depends(database.get_db)):
    """
    Main endpoint to process a user's financial hypothesis.
    """
    result = await run_analysis(request.hypothesis, db)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
