## Greenville Infrastructure Operational Overview
*Describe modifications to municipal GIS pipelines, spatial joins, or TimesFM infrastructure models.*

- [ ] Spatial Projection / Coordinate System (EPSG:2273)
- [ ] Stormwater / Culvert Capacity Simulation
- [ ] Pavement Condition / Road Wear Forecast
- [ ] Municipal Data Dictionary & Medallion Pipeline

## Spatial Accuracy & Coordinate Integrity
- **EPSG:2273 Verified:** Confirmed spatial operations use projected state plane feet.
- **Bounding Box Validated:** Confirmed coordinates fall strictly within Greenville County bounds.

## Verification Checklist
- [ ] Test suite passed (6/6 tests): `python -m pytest tests/ -v`
- [ ] Data files restored and clean
