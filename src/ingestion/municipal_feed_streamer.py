"""
Greenville, SC Infrastructure & Growth Analytics Lakehouse
Municipal & Federal Telemetry Ingestion Streamer (src/ingestion/municipal_feed_streamer.py)
"""

import csv
import json
import math
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.models import (
    GREENVILLE_INFRASTRUCTURE_NODES,
    InfrastructureDomain,
    MunicipalZone
)

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"


class GreenvilleMunicipalStreamer:
    """Simulates high-throughput multi-domain municipal, state, and federal feeds for Greenville County."""

    def __init__(self):
        os.makedirs(RAW_DIR, exist_ok=True)
        os.makedirs(BRONZE_DIR, exist_ok=True)
        os.makedirs(SILVER_DIR, exist_ok=True)

    def generate_historical_telemetry(self, weeks: int = 52) -> Path:
        """Generates 52 weeks of historical time-series across all 8 nodes."""
        raw_csv_path = RAW_DIR / "greenville_infrastructure_telemetry.csv"
        records = []

        base_date = datetime(2025, 3, 1, 0, 0, 0, tzinfo=timezone.utc)

        for w in range(weeks):
            week_date = base_date + timedelta(weeks=w)
            date_str = week_date.strftime("%Y-%m-%d")

            # Seasonal factors (Summer heat peak for grid/water, Fall holiday peak for freight/traffic)
            summer_factor = math.sin((w / 52.0) * 2 * math.pi - (math.pi / 2)) * 0.18 + 1.0
            freight_growth = 1.0 + (w * 0.0035)  # 18% annual growth trend in Inland Port / GSP

            for node_id, node in GREENVILLE_INFRASTRUCTURE_NODES.items():
                if node.domain == InfrastructureDomain.WATER:
                    treated_mgd = round(65.0 * summer_factor + random.uniform(-3.5, 4.2), 2)
                    reservoir_pct = round(92.0 - (summer_factor * 8.5) + random.uniform(-1.5, 1.5), 1)
                    utilization = round((treated_mgd / node.nominal_capacity) * 100, 1)
                    metric_val = treated_mgd
                elif node.domain == InfrastructureDomain.ROADS:
                    aadt = round(node.nominal_capacity * (node.current_utilization_pct / 100.0) * freight_growth + random.uniform(-1200, 1500), 0)
                    vc_ratio = round(aadt / node.nominal_capacity, 2)
                    utilization = round(vc_ratio * 100, 1)
                    metric_val = aadt
                elif node.domain == InfrastructureDomain.RAILWAYS:
                    lifts = round((node.nominal_capacity / 52.0) * freight_growth + random.uniform(-150, 220), 0)
                    utilization = round((lifts / (node.nominal_capacity / 52.0)) * 100, 1)
                    metric_val = lifts
                elif node.domain == InfrastructureDomain.AIRPORT:
                    tons = round((node.nominal_capacity / 52.0) * freight_growth + random.uniform(-80, 110), 1)
                    utilization = round((tons / (node.nominal_capacity / 52.0)) * 100, 1)
                    metric_val = tons
                elif node.domain == InfrastructureDomain.ELECTRICITY:
                    peak_mw = round(320.0 * summer_factor * freight_growth + random.uniform(-12.0, 18.5), 1)
                    utilization = round((peak_mw / node.nominal_capacity) * 100, 1)
                    metric_val = peak_mw
                elif node.domain == InfrastructureDomain.LAND_GROWTH:
                    parcels = round((node.nominal_capacity / 13.0) * freight_growth + random.uniform(-15, 25), 0)
                    utilization = round((parcels / (node.nominal_capacity / 13.0)) * 100, 1)
                    metric_val = parcels
                else:  # TRANSIT_TRAILS
                    trips = round((node.nominal_capacity / 52.0) * summer_factor + random.uniform(-600, 950), 0)
                    utilization = round((trips / (node.nominal_capacity / 52.0)) * 100, 1)
                    metric_val = trips

                records.append({
                    "week_index": w + 1,
                    "reading_date": date_str,
                    "node_id": node.node_id,
                    "node_name": node.name,
                    "domain": node.domain.value,
                    "zone": node.zone.value,
                    "metric_value": metric_val,
                    "unit": node.unit,
                    "capacity_utilization_pct": utilization,
                    "agency_owner": node.agency_owner
                })

        with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "week_index", "reading_date", "node_id", "node_name", "domain",
                "zone", "metric_value", "unit", "capacity_utilization_pct", "agency_owner"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"Generated Raw Municipal Telemetry: {raw_csv_path} ({len(records)} records)")
        return raw_csv_path

    def ingest_to_bronze(self, raw_csv_path: Path) -> Path:
        """Ingests raw CSV stream into append-only Bronze Delta JSON zone."""
        bronze_json_path = BRONZE_DIR / "bronze_municipal_records.json"
        records = []
        with open(raw_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    "raw_payload": row,
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                    "source_system": f"GREENVILLE_OPEN_DATA_{row['domain']}",
                    "schema_version": "2.4.0"
                })

        with open(bronze_json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        print(f"Ingested to Bronze Delta Zone: {bronze_json_path}")
        return bronze_json_path

    def build_silver_mart(self, bronze_json_path: Path) -> Path:
        """Cleanses Bronze records, standardizes timestamps, and builds Silver Curated Mart."""
        silver_mart_path = SILVER_DIR / "silver_infrastructure_mart.json"
        with open(bronze_json_path, "r", encoding="utf-8") as f:
            raw_entries = json.load(f)

        curated = []
        for entry in raw_entries:
            p = entry["raw_payload"]
            utilization = float(p["capacity_utilization_pct"])

            if utilization >= 100.0:
                stress_tier = "CRITICAL_BOTTLENECK"
            elif utilization >= 85.0:
                stress_tier = "HIGH_STRESS"
            elif utilization >= 70.0:
                stress_tier = "MODERATE_STRESS"
            else:
                stress_tier = "HEALTHY_CAPACITY"

            curated.append({
                "week_index": int(p["week_index"]),
                "reading_date": p["reading_date"],
                "node_id": p["node_id"],
                "node_name": p["node_name"],
                "domain": p["domain"],
                "zone": p["zone"],
                "metric_value": float(p["metric_value"]),
                "unit": p["unit"],
                "capacity_utilization_pct": utilization,
                "stress_tier": stress_tier,
                "agency_owner": p["agency_owner"],
                "curated_at": datetime.now(timezone.utc).isoformat()
            })

        with open(silver_mart_path, "w", encoding="utf-8") as f:
            json.dump(curated, f, indent=2)

        print(f"Created Silver Curated Infrastructure Mart: {silver_mart_path}")
        return silver_mart_path


if __name__ == "__main__":
    streamer = GreenvilleMunicipalStreamer()
    raw_csv = streamer.generate_historical_telemetry()
    bronze = streamer.ingest_to_bronze(raw_csv)
    silver = streamer.build_silver_mart(bronze)
