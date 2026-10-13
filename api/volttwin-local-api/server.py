from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from course_model import simulate

app = FastAPI(title="VoltTwin local course-model API", version="1.0")
# Local development only. Do not expose this server to the public internet.
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "null"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])

class SimulationRequest(BaseModel):
    duration_s: float = Field(default=3600, ge=10, le=86400)
    step_s: float = Field(default=10, ge=1, le=3600)
    ambient_c: float = Field(default=25, ge=-20, le=70)
    cycle: str = Field(default="urban", pattern="^(urban|highway|idle)$")
    fan_duty: float = Field(default=0, ge=0, le=1)
    seed: int = Field(default=42, ge=0, le=1000000)

@app.get("/api/health")
def health():
    return {"status": "ok", "model": "course Day 1 battery physics (PackParams + RK4)", "demo_simulation": False}

@app.post("/api/simulate")
def run_simulation(req: SimulationRequest):
    if req.step_s > req.duration_s:
        raise HTTPException(status_code=400, detail="step_s must be no greater than duration_s")
    try:
        df = simulate(T_end=req.duration_s, dt=req.step_s, cycle=req.cycle, T_amb=req.ambient_c, fan_duty=req.fan_duty, seed=req.seed)
        rows = df.to_dict(orient="records")
        last = rows[-1]
        return {"source": "course_day01_physics_model", "units": {"t":"s", "SoC":"fraction (0-1)", "T":"degC", "Q":"Ah", "R":"ohm", "u":"fraction (0-1)", "I":"A"}, "summary": {"temperature_c": round(last["T"], 4), "soc_percent": round(last["SoC"]*100, 4), "capacity_ah": round(last["Q"], 6), "resistance_ohm": round(last["R"], 8), "current_a": round(last["I"], 4), "fan_duty_percent": round(last["u"]*100, 2), "samples": len(rows)}, "series": rows}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
