"""Transparent Monte Carlo accommodation scenario engine; assumptions are user supplied."""
from __future__ import annotations
import numpy as np


def simulate_project(rooms: int, adr_pkr: float, occupancy_pct: float,
                     annual_fixed_cost_pkr: float, capex_pkr: float,
                     years: int = 10, simulations: int = 5000,
                     discount_rate_pct: float = 15.0, seed: int = 42) -> dict:
    if rooms < 1 or adr_pkr <= 0 or annual_fixed_cost_pkr < 0 or capex_pkr <= 0:
        raise ValueError("Rooms and ADR must be positive; costs cannot be negative; capex must be positive.")
    if not 0 < occupancy_pct < 100 or not 0 <= discount_rate_pct < 100:
        raise ValueError("Occupancy must be between 0 and 100; discount rate must be 0–99%.")
    if not 1 <= years <= 20 or simulations < 500:
        raise ValueError("Use 1–20 projection years and at least 500 simulations.")
    rng = np.random.default_rng(seed)
    n = simulations
    adr = np.full(n, float(adr_pkr))
    occ = np.clip(rng.normal(occupancy_pct / 100, 0.07, n), 0.05, 0.95)
    costs = np.full(n, float(annual_fixed_cost_pkr))
    initial = capex_pkr * rng.lognormal(mean=-0.5 * 0.10**2, sigma=0.10, size=n)
    discount = 1 + discount_rate_pct / 100
    npv = -initial.copy()
    annual_cash = []
    for year in range(1, years + 1):
        adr *= rng.normal(1.07, 0.035, n)
        occ = np.clip(occ + rng.normal(0.005, 0.025, n), 0.03, 0.96)
        costs *= rng.normal(1.075, 0.025, n)
        revenue = rooms * 365 * occ * adr
        ebitda = revenue - costs
        cash = ebitda - (revenue * 0.03)  # replacement reserve proxy, disclosed
        annual_cash.append(float(np.median(cash)))
        npv += cash / (discount ** year)
    positive = npv > 0
    roi = npv / initial * 100
    return {
        "npv_p10": float(np.percentile(npv, 10)),
        "npv_p50": float(np.percentile(npv, 50)),
        "npv_p90": float(np.percentile(npv, 90)),
        "positive_npv_probability": float(positive.mean() * 100),
        "roi_p50_pct": float(np.percentile(roi, 50)),
        "annual_median_cashflow": annual_cash,
        "years": years,
        "simulations": simulations,
        "assumptions": {
            "ADR annual growth": "Normal(7.0%, 3.5% volatility)",
            "Occupancy change": "Normal(+0.5 percentage points, 2.5 points volatility)",
            "Operating cost inflation": "Normal(7.5%, 2.5% volatility)",
            "Initial capex overrun": "Lognormal, 4% log-mean and 10% sigma",
            "Replacement reserve": "3% of room revenue",
            "Discount rate": f"{discount_rate_pct:.1f}% (user input)",
        },
    }
