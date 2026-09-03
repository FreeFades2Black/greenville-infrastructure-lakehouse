"""
Greenville, SC Infrastructure & Growth Analytics Lakehouse
End-to-End Medallion Lakehouse Pipeline (src/processing/delta_lakehouse.py)
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.municipal_feed_streamer import GreenvilleMunicipalStreamer
from src.analytics.spatial_bottleneck_diagnostics import GreenvilleBottleneckDiagnostics
from src.analytics.timesfm_infrastructure_forecaster import TimesFM3InfrastructureForecaster
from src.analytics.counterfactual_policy_engine import GreenvilleCounterfactualPolicyEngine


class GreenvilleInfrastructureLakehousePipeline:
    """Orchestrates end-to-end Medallion data engineering and predictive policy intelligence."""

    def __init__(self):
        self.streamer = GreenvilleMunicipalStreamer()
        self.diagnostics = GreenvilleBottleneckDiagnostics()
        self.forecaster = TimesFM3InfrastructureForecaster()
        self.policy_engine = GreenvilleCounterfactualPolicyEngine()

    def run_full_pipeline(self):
        print("=" * 80)
        print("  STARTING GREENVILLE, SC INFRASTRUCTURE & GROWTH LAKEHOUSE PIPELINE")
        print("=" * 80)

        # 1. Ingestion
        print("\n[STEP 1/4] Ingesting REAL USGS Water, SCDOT Traffic, SC Ports, and Census Feeds...")
        bronze_json = self.streamer.ingest_real_cross_domain_telemetry()
        silver_mart = self.streamer.build_silver_mart(bronze_json)

        # 2. Diagnostics
        print("\n[STEP 2/4] Executing Spatial Divergence & Cross-Domain Bottleneck Diagnostics...")
        diag_dossier = self.diagnostics.execute_diagnostics()

        # 3. Foundation Forecasting
        print("\n[STEP 3/4] Executing Google TimesFM-3 52-Week Foundation Infrastructure Forecaster...")
        takt_dossier = self.forecaster.generate_52w_forecast()

        # 4. Counterfactual Policy Engine
        print("\n[STEP 4/4] Evaluating Counterfactual Policy Simulations & CIP Interventions...")
        policy_dossier = self.policy_engine.evaluate_policy_interventions()

        print("\n" + "=" * 80)
        print("  PIPELINE COMPLETE: SUCCESS")
        print(f"  Critical Bottlenecks: {diag_dossier['executive_diagnostic_summary']['critical_bottleneck_zones']}")
        print(f"  TimesFM-3 52W Forecast: Generated ({takt_dossier['metadata']['mean_absolute_percentage_error_mape']}% MAPE)")
        print(f"  Avoided CIP Capital Expenditure: {policy_dossier['executive_policy_scorecard']['total_cip_capital_savings_usd']}")
        print("=" * 80)

        return {
            "pipeline_status": "SUCCESS",
            "bronze_path": str(bronze_json),
            "silver_path": str(silver_mart),
            "diagnostics": diag_dossier,
            "forecast": takt_dossier,
            "policy": policy_dossier
        }


if __name__ == "__main__":
    pipeline = GreenvilleInfrastructureLakehousePipeline()
    pipeline.run_full_pipeline()
