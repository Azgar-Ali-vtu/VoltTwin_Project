# VoltTwin — Battery Digital Twin Dashboard

A standalone, responsive browser dashboard prototype based on the uploaded Digital Twin with Python course materials, especially the Day 5 operator dashboard and final-project brief.

## Run it
1. Extract `battery-digital-twin-dashboard.zip`.
2. Open `index.html` in a modern browser (Chrome, Edge, or Firefox).
3. Use the sidebar to switch pages.

No installation, external library, server, or internet connection is required.

## Included interactive features
- Thermal simulation demo with ambient temperature, initial temperature, sensor noise, time step, fan ramp, and temperature limit controls.
- Fault injection for cooling degradation, sensor bias, and missing packets.
- Operator overview with temperature chart, state indicators, fan duty, trust estimate, and alarms.
- Telemetry chart and table, residual/CUSUM demonstration, event history.
- JSON, JSONL, and CSV exports.
- Credibility scorecard with explicit open gaps.
- Architecture view showing data and control flow.

## Important limitations
- This is a frontend-only educational prototype. The simulation runs in JavaScript in the browser; it is not connected to the course's Python notebook, a real battery, BMS, or physical sensors.
- Battery voltage and state-of-charge values are illustrative indicators, not validated electrical or electrochemical models.
- The trust score, maturity label, and residual detector are demonstration logic, not safety-certified or validated metrics.
- The displayed `demo:` fingerprint is a deterministic configuration identifier, not a cryptographic SHA-256 digest.
- The credibility scorecard deliberately leaves convergence testing, calibration identifiability/uncertainty, baseline validation, and independent physical validation open.
- Do not use this prototype to operate or assess real batteries.

## Suggested next engineering step
Connect a Python simulation based on the course notebook to a FastAPI backend, and replace the browser demo model with API-fed telemetry. Then validate the model and detector using reproducible notebook tests and reference datasets.
