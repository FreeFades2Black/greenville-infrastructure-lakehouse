"""
Greenville, SC Infrastructure & Growth Analytics Lakehouse
Unit & Integration Test Suite (tests/test_greenville_lakehouse.py)
"""

import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.models import (
    InfrastructureDomain,
    MunicipalZone,
    GREENVILLE_INFRASTRUCTURE_NODES
)
from src.ingestion.municipal_feed_streamer import GreenvilleMunicipalStreamer
from src.analytics.spatial_bottleneck_diagnostics import GreenvilleBottleneckDiagnostics
from src.analytics.timesfm_infrastructure_forecaster import TimesFM3InfrastructureForecaster
from src.analytics.counterfactual_policy_engine import GreenvilleCounterfactualPolicyEngine
from src.processing.delta_lakehouse import GreenvilleInfrastructureLakehousePipeline


def test_models_and_node_specifications():
    """Verify 7 domains and 8 Greenville infrastructure landmark nodes."""
    assert len(GREENVILLE_INFRASTRUCTURE_NODES) == 8
    assert "NODE_WAT_01" in GREENVILLE_INFRASTRUCTURE_NODES
    assert "NODE_ROA_01" in GREENVILLE_INFRASTRUCTURE_NODES
    assert "NODE_RAI_01" in GREENVILLE_INFRASTRUCTURE_NODES

    water_node = GREENVILLE_INFRASTRUCTURE_NODES["NODE_WAT_01"]
    assert water_node.domain == InfrastructureDomain.WATER
    assert water_node.nominal_capacity == 135.0


def test_municipal_feed_ingestion_and_silver_mart():
    """Verify municipal telemetry generation, Bronze Delta ingestion, and Silver Mart creation."""
    streamer = GreenvilleMunicipalStreamer()
    raw_csv = streamer.generate_historical_telemetry(weeks=12)
    bronze_path = streamer.ingest_to_bronze(raw_csv)
    silver_path = streamer.build_silver_mart(bronze_path)

    assert bronze_path.exists()
    assert silver_path.exists()


def test_spatial_bottleneck_diagnostics():
    """Verify spatial divergence (>25% discrepancy) and cross-correlations."""
    diagnostics = GreenvilleBottleneckDiagnostics()
    dossier = diagnostics.execute_diagnostics()

    assert "executive_diagnostic_summary" in dossier
    assert dossier["executive_diagnostic_summary"]["land_utility_discrepancy_score_pct"] > 25.0
    assert len(dossier["bottleneck_diagnostics_matrix"]) == 3


def test_timesfm_infrastructure_forecaster():
    """Verify Google TimesFM-3 produces 52-week forward projections with P10/P50/P90 quantile bounds."""
    forecaster = TimesFM3InfrastructureForecaster()
    dossier = forecaster.generate_52w_forecast()

    assert "predictive_infrastructure_scorecard" in dossier
    trajectory = dossier["forecast_trajectory"]
    assert len(trajectory["timeline_weeks"]) == 52

    for i in range(len(trajectory["timeline_weeks"])):
        p10 = trajectory["i85_forecast_lower_bound_p10"][i]
        p50 = trajectory["i85_forecast_p50_index"][i]
        p90 = trajectory["i85_forecast_upper_bound_p90"][i]
        assert p10 <= p50 <= p90


def test_counterfactual_policy_simulations():
    """Verify counterfactual simulation of UGB, rail grade separation, and BESS microgrids."""
    engine = GreenvilleCounterfactualPolicyEngine()
    dossier = engine.evaluate_policy_interventions()

    assert "executive_policy_scorecard" in dossier
    assert dossier["executive_policy_scorecard"]["arterial_queue_reduction_pct"] == 34.0
    assert len(dossier["counterfactual_policy_matrix"]) == 3


def test_full_lakehouse_pipeline():
    """Verify end-to-end Medallion execution."""
    pipeline = GreenvilleInfrastructureLakehousePipeline()
    result = pipeline.run_full_pipeline()

    assert result["pipeline_status"] == "SUCCESS"
    assert "diagnostics" in result
    assert "forecast" in result
    assert "policy" in result
