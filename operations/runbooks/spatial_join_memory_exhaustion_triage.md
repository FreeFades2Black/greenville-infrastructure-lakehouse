# Operational Runbook: Diagnosing Spatial Join Memory Overhead & Cartesian Skew

**Severity:** P2 / Pipeline Stalled  
**Target Systems:** PostGIS / Apache Sedona, PySpark Spatial Join Engine

## Diagnostic Workflow

### 1. Identify Spatial Skew in Parcels vs Road Buffers
```bash
python -m src.pipeline --diagnose-spatial-skew
```

### 2. Verify Spatial Indexing (R-Tree / Quadtree)
Check that geometric columns maintain bounding box spatial indices:
```python
# Verify spatial grid partitioning
df.explain()
```

### 3. Step-by-Step Remediation
1. If spatial join exhausts executor memory, enable spatial grid partitioning:
   ```python
   # Set spatial partition grid size to 100x100
   spark.conf.set("sedona.join.gridtype", "quadtree")
   ```
2. Re-run verification test suite:
   ```bash
   python -m pytest tests/test_greenville_lakehouse.py -v
   ```
