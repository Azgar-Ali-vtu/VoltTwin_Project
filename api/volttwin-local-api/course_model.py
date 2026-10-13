"""Battery physics model adapted from the course's Day 1 notebook.
Original course material: digital-twin-veltech-NB-lecture, NB01_concept_and_architecture.ipynb.
The equations and defaults below are the course model; this module omits notebook-only plots/widgets.
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class PackParams:
    Q0: float = 60.0
    R0: float = 0.045
    m_cp: float = 9000.0
    hA0: float = 2.2
    hA1: float = 12.0
    k_age: float = 5.5e-8
    Ea_R: float = 3800.0
    T_ref: float = 298.15
    fan_W: float = 25.0

def pack_derivatives(t, x, I, u, T_amb, p: PackParams):
    SoC, T, Q, R = x
    T_K = T + 273.15
    P_gen = I ** 2 * R
    P_cool = (p.hA0 + p.hA1 * u) * (T - T_amb)
    arrh = np.exp(-p.Ea_R * (1.0 / T_K - 1.0 / p.T_ref))
    dSoC = -I / (3600.0 * max(Q, 1e-6))
    dT = (P_gen - P_cool) / p.m_cp
    dQ = -p.k_age * abs(I) * arrh
    dR = p.R0 * 0.9 * (p.Q0 - Q) / p.Q0 * 1e-3
    return np.array([dSoC, dT, dQ, dR])

def duty_cycle(t, kind="urban", seed=42):
    if kind == "urban":
        base = 14 + 26 * (np.sin(2 * np.pi * t / 420.0) > 0.15)
        regen = -18 * (np.sin(2 * np.pi * t / 420.0 + 0.9) > 0.93)
        return base + regen
    if kind == "highway":
        return 40 + 6 * np.sin(2 * np.pi * t / 1800.0)
    if kind == "idle":
        return 8.0
    raise ValueError("cycle must be urban, highway, or idle")

def rk4_step(fun, t, x, dt, *args):
    k1 = fun(t, x, *args)
    k2 = fun(t + dt / 2, x + dt / 2 * k1, *args)
    k3 = fun(t + dt / 2, x + dt / 2 * k2, *args)
    k4 = fun(t + dt, x + dt * k3, *args)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

def simulate(p=None, T_end=3600.0, dt=10.0, cycle="urban", T_amb=25.0, fan_duty=0.0, seed=42):
    """Run the course's physical battery model for a bounded duration."""
    p = p or PackParams()
    if dt <= 0 or T_end <= 0 or T_end > 24 * 3600 or dt > T_end:
        raise ValueError("Use 0 < dt <= T_end <= 86400 seconds")
    n = int(T_end / dt)
    if n < 1 or n > 20000:
        raise ValueError("Simulation must contain between 1 and 20,000 steps")
    fan_duty = float(np.clip(fan_duty, 0.0, 1.0))
    x = np.array([0.95, T_amb + 1.0, p.Q0, p.R0], dtype=float)
    rows = []
    for k in range(n + 1):
        t = k * dt
        I = float(duty_cycle(t, cycle, seed))
        rows.append({"t": t, "SoC": float(x[0]), "T": float(x[1]), "Q": float(x[2]), "R": float(x[3]), "u": fan_duty, "I": I})
        if k == n:
            break
        x = rk4_step(pack_derivatives, t, x, dt, I, fan_duty, T_amb, p)
        x[0] = np.clip(x[0], 0.0, 1.0)
    return pd.DataFrame(rows)
