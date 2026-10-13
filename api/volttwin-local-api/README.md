# VoltTwin local Python API — beginner setup

This starter exposes the course's Day 1 battery physics model as a local API. It uses the course's PackParams, pack_derivatives, duty_cycle, and RK4 integration equations, with notebook plotting/widgets removed. It is **not yet the complete Day 5 DigitalTwin orchestration / full dashboard wiring**; this is the first safe step to prove the real course model runs on your laptop.

## 1. Install Python
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/windows/.
2. During setup, tick **Add python.exe to PATH**.
3. Open Command Prompt and type `py --version`. You should see Python 3.11.x or 3.12.x.

## 2. Start the API
1. Extract this folder somewhere easy, e.g. Desktop.
2. Double-click `start_server.bat`.
3. Wait until the terminal says Uvicorn is running at `http://127.0.0.1:8000`. Keep that window open.
4. Open http://127.0.0.1:8000/docs in Chrome. This is a test page for the API.
5. Expand `GET /api/health`, click **Try it out**, then **Execute**. The response should say `status: ok` and `demo_simulation: false`.
6. Expand `POST /api/simulate`, click **Try it out**, and use this example:
   {
     "duration_s": 3600,
     "step_s": 10,
     "ambient_c": 25,
     "cycle": "urban",
     "fan_duty": 0.3,
     "seed": 42
   }
7. Click **Execute**. The response should contain `source: course_day01_physics_model`, `summary`, and `series` with temperature, SoC, capacity, resistance, current, and fan duty.

## 3. Important notes
- Keep the server bound to `127.0.0.1`; do not change it to `0.0.0.0` or expose it to the internet.
- This endpoint runs the course's physical battery model. The fixed `fan_duty` is an input for this initial API; the course's full closed-loop DigitalTwin/controller will be the next integration stage.
- The dashboard HTML is intentionally not overwritten by this starter. Once the API test succeeds, the next step is to wire VoltTwin's New run / charts to `POST /api/simulate`, replacing the browser demo path while preserving the UI.
