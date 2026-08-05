from pathlib import Path
import traceback
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from backend import run_travel_agent

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="TripMate AI",
    description="LangGraph Multi-Agent Travel Planner with FastAPI Frontend",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)



class TravelRequest(BaseModel):
    message: str
    thread_id: str | None = None



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


class TravelRequest(BaseModel):
    departure: str | None = None
    arrival: str | None = None
    days: int | None = None
    details: str | None = None
    thread_id: str | None = None


def build_travel_query(departure, arrival, days, details) -> str:
    """
    Construit une requête textuelle propre et non ambiguë
    à partir des champs structurés fournis par l'utilisateur.
    """
    parts = []

    if departure and arrival:
        parts.append(f"Vols de {departure.strip()} à {arrival.strip()}.")
    elif departure:
        parts.append(f"Vols au départ de {departure.strip()}.")
    elif arrival:
        parts.append(f"Vols à destination de {arrival.strip()}.")

    if days:
        parts.append(f"Durée du séjour : {days} jours.")

    if details:
        parts.append(details.strip())

    return " ".join(parts).strip()


@app.post("/api/travel")
async def travel_planner(request_data: TravelRequest):
    try:
        user_message = build_travel_query(
            request_data.departure,
            request_data.arrival,
            request_data.days,
            request_data.details,
        )

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Merci de préciser au moins un départ, une arrivée ou des détails."
                }
            )

        result = run_travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id
        )

        return JSONResponse(
            content={
                "success": True,
                "thread_id": result["thread_id"],
                "answer": result["answer"],
                "flight_results": result["flight_results"],
                "hotel_results": result["hotel_results"],
                "itinerary": result["itinerary"],
                "llm_calls": result["llm_calls"],
            }
        )

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "AI Travel Planner API is running"
    }


@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={})



if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )