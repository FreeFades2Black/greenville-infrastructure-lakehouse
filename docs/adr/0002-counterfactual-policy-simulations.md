# ADR-0002: Pre-Computing Counterfactual Civil Policy Simulations into Gold Delta Tables

**Status:** Accepted  
**Date:** 2026-06-24  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
City planners and civil engineers require interactive scenario modeling (e.g. impact of a 100-year storm surge on Reedy River culverts, or repaving priority optimization given budget cuts). Running full spatial hydraulic simulations at query time timed out GIS dashboards.

## 2. Options Considered
* **Option A: Real-Time Dynamic Simulation Compute on Dashboard Request**
  - *Evaluation:* Highly flexible, but takes 45-90 seconds per query, exhausting dashboard connection pools and frustrating municipal planners.
* **Option B: Batch Pre-Computation of Counterfactual Simulation Matrices in Gold Delta Marts**
  - *Evaluation:* Nightly PySpark batch runs iterate through 24 standardized civil policy and rainfall scenarios; dashboard queries retrieve pre-computed scenarios in under 80ms via partition keys.

## 3. Decision & Trade-Off Accepted
We adopted **Option B (Pre-Computed Gold Marts)**.  
**Trade-Off Accepted:** Requires ~45 minutes of overnight batch compute; parameters are constrained to discrete policy steps.
