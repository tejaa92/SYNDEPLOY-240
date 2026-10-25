#!/usr/bin/env python3
"""SYNDEPLOY-240: Synthetic Multi-Site Industrial IoT Deployment Planning Dataset.

Generates 240 fully synthetic manufacturing site records for research on
multi-site industrial IoT deployment planning (readiness assessment, rollout
wave sequencing, planning-tool prototyping).

EVERY record is synthetic and EVERY outcome variable is simulated by the
documented model below. No record describes any real site, company, or
program. Do not use this dataset as evidence about any real deployment.

Generation model (seed 42, Python standard library only):
- Each site gets a plant archetype. Archetypes shift the mean of the six
  readiness dimension scores (0-100, normal, sd 12, clipped to [5, 98]):
    archetype means (network, data_quality, ot_security, leadership,
                     workforce, change_capacity)
    discrete_assembly: (68, 60, 58, 66, 62, 60)
    machining:         (58, 52, 55, 60, 55, 54)
    process:           (72, 66, 70, 64, 60, 58)
    fabrication:       (54, 50, 52, 58, 56, 52)
- Installed-base flags correlate with network readiness:
  historian_present p = 0.25 + 0.006*network; mes_present p = 0.2 + 0.006*network;
  erp_present p = 0.55 + 0.003*network.
- readiness_composite = weighted mean of the six dimensions with weights
  network .20, data_quality .20, ot_security .15, leadership .15,
  workforce .15, change_capacity .15 (rounded to 1 decimal).
- readiness_tier: high >= 65, medium 50-64.9, low < 50.
- assigned_wave (gated rule): wave 1 if composite >= 70 and min dimension
  >= 50; wave 2 if composite >= 58; wave 3 if composite >= 45; else wave 4
  (remediation track first).
- Simulated outcomes (functions of readiness + noise; formulas published in
  the descriptor paper):
    sim_onboarding_weeks  = round(26 - 0.16*composite + N(0, 2.5)), min 4
    sim_blocker_events    = max(0, round(9 - 0.09*composite + N(0, 1.8)))
    sim_data_completeness_pct = clip(round(38 + 0.58*data_quality + N(0, 5)), 5, 99)
    sim_adoption_6mo_pct  = clip(round(8 + 0.55*leadership + 0.35*workforce
                                      + N(0, 6)), 2, 98)
Outputs: syndeploy240_sites.csv, syndeploy240_sites.json, and prints the
SHA-256 of the CSV for the reproducibility record.
"""

import csv
import hashlib
import json
import random
from pathlib import Path

SEED = 42
N_SITES = 240
OUT_DIR = Path(__file__).resolve().parent

ARCHETYPES = {
    "discrete_assembly": (68, 60, 58, 66, 62, 60),
    "machining": (58, 52, 55, 60, 55, 54),
    "process": (72, 66, 70, 64, 60, 58),
    "fabrication": (54, 50, 52, 58, 56, 52),
}
ARCHETYPE_KEYS = list(ARCHETYPES.keys())
SIZE_BANDS = ["small_50_249", "medium_250_999", "large_1000_plus"]
REGION_BANDS = ["north", "south", "east", "west", "central"]
WEIGHTS = (0.20, 0.20, 0.15, 0.15, 0.15, 0.15)

FIELDS = [
    "site_id", "plant_archetype", "size_band", "region_band",
    "production_lines", "equipment_count", "avg_equipment_age_years",
    "pct_equipment_network_ready", "historian_present", "mes_present",
    "erp_present", "network_score", "data_quality_score", "ot_security_score",
    "leadership_engagement_score", "workforce_readiness_score",
    "change_capacity_score", "maintenance_maturity_1_5", "prior_pilot",
    "readiness_composite", "readiness_tier", "assigned_wave",
    "sim_onboarding_weeks", "sim_blocker_events", "sim_data_completeness_pct",
    "sim_adoption_6mo_pct",
]


def clip(v, lo, hi):
    return max(lo, min(hi, v))


def main():
    rng = random.Random(SEED)
    rows = []
    for i in range(1, N_SITES + 1):
        arch = ARCHETYPE_KEYS[(i - 1) % len(ARCHETYPE_KEYS)]
        means = ARCHETYPES[arch]
        scores = [clip(round(rng.gauss(m, 12)), 5, 98) for m in means]
        network, dq, otsec, lead, workf, change = scores

        size = rng.choice(SIZE_BANDS)
        equip = {"small_50_249": rng.randint(40, 220),
                 "medium_250_999": rng.randint(180, 640),
                 "large_1000_plus": rng.randint(500, 1600)}[size]
        lines = max(1, round(equip / rng.randint(55, 95)))

        composite = round(sum(s * w for s, w in zip(scores, WEIGHTS)), 1)
        tier = "high" if composite >= 65 else ("medium" if composite >= 50 else "low")
        min_dim = min(scores)
        if composite >= 70 and min_dim >= 50:
            wave = 1
        elif composite >= 58:
            wave = 2
        elif composite >= 45:
            wave = 3
        else:
            wave = 4

        rows.append({
            "site_id": f"SYN-SITE-{i:03d}",
            "plant_archetype": arch,
            "size_band": size,
            "region_band": rng.choice(REGION_BANDS),
            "production_lines": lines,
            "equipment_count": equip,
            "avg_equipment_age_years": round(clip(rng.gauss(14, 6), 2, 38), 1),
            "pct_equipment_network_ready": clip(round(rng.gauss(20 + 0.65 * network, 10)), 2, 99),
            "historian_present": int(rng.random() < 0.25 + 0.006 * network),
            "mes_present": int(rng.random() < 0.20 + 0.006 * network),
            "erp_present": int(rng.random() < 0.55 + 0.003 * network),
            "network_score": network,
            "data_quality_score": dq,
            "ot_security_score": otsec,
            "leadership_engagement_score": lead,
            "workforce_readiness_score": workf,
            "change_capacity_score": change,
            "maintenance_maturity_1_5": rng.randint(1, 5),
            "prior_pilot": int(rng.random() < 0.35),
            "readiness_composite": composite,
            "readiness_tier": tier,
            "assigned_wave": wave,
            "sim_onboarding_weeks": max(4, round(26 - 0.16 * composite + rng.gauss(0, 2.5))),
            "sim_blocker_events": max(0, round(9 - 0.09 * composite + rng.gauss(0, 1.8))),
            "sim_data_completeness_pct": clip(round(38 + 0.58 * dq + rng.gauss(0, 5)), 5, 99),
            "sim_adoption_6mo_pct": clip(round(8 + 0.55 * lead + 0.35 * workf + rng.gauss(0, 6)), 2, 98),
        })

    csv_path = OUT_DIR / "syndeploy240_sites.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    with open(OUT_DIR / "syndeploy240_sites.json", "w") as f:
        json.dump(rows, f, indent=1)

    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    print(f"rows={len(rows)} csv_sha256={digest}")
    return digest


if __name__ == "__main__":
    main()
