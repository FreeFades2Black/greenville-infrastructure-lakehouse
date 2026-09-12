# ADR-0001: Standardization on EPSG:2273 (NAD83 South Carolina State Plane) for Spatial Joins

**Status:** Accepted  
**Date:** 2026-06-03  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
Municipal civil infrastructure analytics (stormwater runoff, pavement condition index, sewer line maintenance) across Greenville County requires spatial joins between county parcels, road centerlines, and watershed boundaries.

## 2. Options Considered
* **Option A: Unprojected Geographic Coordinates (WGS84 EPSG:4326 in Decimal Degrees)**
  - *Evaluation:* Standard GPS format, but Euclidean distance calculations in decimal degrees introduce severe spatial distortion (~15% distance error) and require expensive haversine trigonometry in queries.
* **Option B: Projected Coordinate System EPSG:2273 (NAD83 / South Carolina State Plane International Feet)**
  - *Evaluation:* Conformal projection preserves angles and delivers sub-foot linear distance accuracy across Greenville County; enables direct Cartesian geometry joins (`ST_DWithin`).

## 3. Decision & Trade-Off Accepted
We adopted **Option B (EPSG:2273)**.  
**Trade-Off Accepted:** Inbound GPS telemetry from maintenance trucks (WGS84) must be reprojected during Bronze-to-Silver ETL (`ST_Transform(geom, 2273)`); reprojection cost is ~2ms per 1,000 coordinates.
