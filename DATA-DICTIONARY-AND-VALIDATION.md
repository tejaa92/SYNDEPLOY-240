# SYNDEPLOY-240 - Data Dictionary and Validation Record

Dataset: Synthetic Multi-Site Industrial IoT Deployment Planning Dataset, v1.0 (generated October 20, 2026).
Files: syndeploy240_sites.csv (27.6 KB), syndeploy240_sites.json (181.7 KB), generate_dataset.py (generator, Python 3 standard library, seed 42).
Reproducibility: CSV SHA-256 a55592a8cefa01f467041ec8fa2e0f5838b46a51b84338cf301961ecf7c1a872, identical across two independent runs of the generator (verified Oct 20, 2026).
Status: NOT yet deposited. Planned deposit: Zenodo (DOI) + GitHub (code), CC BY 4.0, at paper submission time.

## Critical framing
Every record is synthetic. Every outcome variable (fields prefixed sim_) is simulated by the published generation model in generate_dataset.py. No record describes any real site, company, plant, or program, and the dataset must never be cited as evidence about a real deployment. Its purpose is methods research: testing rollout-sequencing approaches, benchmarking readiness models, and prototyping deployment-planning tools.

## Fields (26)
Identity and archetype:
- site_id: synthetic identifier, SYN-SITE-001 to SYN-SITE-240.
- plant_archetype: discrete_assembly, machining, process, or fabrication (60 sites each, by construction).
- size_band: small_50_249, medium_250_999, or large_1000_plus (employee band).
- region_band: north, south, east, west, or central (abstract bands only; no real geography).
- production_lines: integer count, derived from equipment count.
- equipment_count: integer, drawn within the size band's range.
- avg_equipment_age_years: float, 2 to 38.
- pct_equipment_network_ready: integer percent, modeled from network readiness.
Installed base (0/1 flags, probabilities increase with network score):
- historian_present, mes_present, erp_present.
Readiness dimension scores (integers 5-98, normal draws around archetype means, sd 12):
- network_score, data_quality_score, ot_security_score, leadership_engagement_score, workforce_readiness_score, change_capacity_score.
Context:
- maintenance_maturity_1_5: integer 1-5. prior_pilot: 0/1.
Derived (documented formulas, recomputed in validation):
- readiness_composite: weighted mean of the six dimensions (weights 0.20, 0.20, 0.15, 0.15, 0.15, 0.15), 1 decimal.
- readiness_tier: high (>= 65), medium (50-64.9), low (< 50).
- assigned_wave: gated rule: wave 1 if composite >= 70 and every dimension >= 50; wave 2 if composite >= 58; wave 3 if composite >= 45; otherwise wave 4 (remediation first).
Simulated outcomes (published functions of readiness plus gaussian noise; see generator header):
- sim_onboarding_weeks, sim_blocker_events, sim_data_completeness_pct, sim_adoption_6mo_pct.

## Validation results (Oct 20, 2026)
- Schema and range checks: all 240 records, all fields in range. Pass.
- Internal consistency: readiness_composite recomputed from dimension scores for all records, 0 mismatches. Tier thresholds re-derived, 0 mismatches. Wave rule re-derived independently, 0 mismatches.
- Distributions: archetypes 60/60/60/60. Tiers: high 59, medium 159, low 22. Waves: 1 = 13, 2 = 128, 3 = 93, 4 = 6.
- Outcome behavior (means by tier, expected monotone direction confirmed): onboarding weeks high 15.1 / medium 16.6 / low 18.1; blocker events 2.2 / 4.0 / 4.4; data completeness 78.4 / 70.4 / 65.2; 6-month adoption 68.7 / 62.5 / 54.9.
- Reproducibility: seed-fixed regeneration reproduces the CSV byte-for-byte (matching SHA-256).

## Known limitations (to be stated in the paper)
Synthetic records shaped by one documented model; outcome relationships are assumptions of that model, not measurements. Archetype distributions are judgment-based, informed by practitioner knowledge of the problem space, not fitted to operational data. Suitable for methods development and prototyping; not suitable for operational, investment, or policy decisions.
