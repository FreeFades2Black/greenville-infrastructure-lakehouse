# Incident Post-Mortem: Coordinate Projection Mismatch in Stormwater Culvert Simulation

**Incident Date:** 2026-08-01  
**Impact Duration:** 35 minutes  
**Severity:** SEV-3  
**Root Cause:** A newly ingested county drainage ditch shapefile declared its projection as EPSG:4326 while coordinates were encoded in EPSG:2273 State Plane Feet. The spatial join treated foot coordinates as decimal degrees, placing drainage culverts in the Indian Ocean and distorting stormwater risk models.

## Timeline
* **10:00 UTC:** GIS ingestion batch processed Greenville County drainage shapefile.
* **10:15 UTC:** Gold counterfactual simulation reported 0 culverts impacted by 50-year flood event.
* **10:24 UTC:** Civil engineer flagged impossible anomaly on Reedy River basin.
* **10:38 UTC:** Incident triage identified bounding box range (`[1.5e6, 1.1e6]`) inconsistent with latitude/longitude.
* **10:45 UTC:** Ingestion script updated with strict coordinate boundary assertions (`-83.0 < lon < -82.0`).

## Corrective Actions
1. Added spatial bounding box validation contract in `test_greenville_lakehouse.py`.
2. Implemented automated projection header validation prior to Silver layer insertion.
