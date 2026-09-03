"""
Greenville, SC Infrastructure & Growth Analytics Lakehouse
Domain Models and Municipal Telemetry Schemas (src/ingestion/models.py)
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class InfrastructureDomain(str, Enum):
    LAND_GROWTH = "LAND_GROWTH"
    WATER = "WATER"
    ELECTRICITY = "ELECTRICITY"
    ROADS = "ROADS"
    RAILWAYS = "RAILWAYS"
    AIRPORT = "AIRPORT"
    TRANSIT_TRAILS = "TRANSIT_TRAILS"


class MunicipalZone(str, Enum):
    DOWNTOWN_GREENVILLE = "DOWNTOWN_GREENVILLE"
    SIMPSONVILLE_SPRAWL = "SIMPSONVILLE_SPRAWL"
    MAULDIN_URBAN_CORE = "MAULDIN_URBAN_CORE"
    GREER_INLAND_PORT = "GREER_INLAND_PORT"
    GSP_AEROSPACE_CORRIDOR = "GSP_AEROSPACE_CORRIDOR"
    WOODRUFF_ROAD_COMMERCIAL = "WOODRUFF_ROAD_COMMERCIAL"
    TABLE_ROCK_WATERSHED = "TABLE_ROCK_WATERSHED"
    SWAMP_RABBIT_CORRIDOR = "SWAMP_RABBIT_CORRIDOR"


class InfrastructureNode(BaseModel):
    node_id: str
    name: str
    domain: InfrastructureDomain
    zone: MunicipalZone
    latitude: float
    longitude: float
    nominal_capacity: float
    unit: str
    current_utilization_pct: float
    bottleneck_risk_tier: str  # LOW, MODERATE, HIGH, CRITICAL
    agency_owner: str


# 8 Key Greenville County Infrastructure Landmark Nodes
GREENVILLE_INFRASTRUCTURE_NODES: Dict[str, InfrastructureNode] = {
    "NODE_WAT_01": InfrastructureNode(
        node_id="NODE_WAT_01",
        name="Table Rock & North Saluda Reservoirs",
        domain=InfrastructureDomain.WATER,
        zone=MunicipalZone.TABLE_ROCK_WATERSHED,
        latitude=35.0340,
        longitude=-82.6015,
        nominal_capacity=135.0,  # Million Gallons / Day (MGD)
        unit="MGD Safe Yield",
        current_utilization_pct=68.4,
        bottleneck_risk_tier="LOW",
        agency_owner="Greenville Water"
    ),
    "NODE_ROA_01": InfrastructureNode(
        node_id="NODE_ROA_01",
        name="I-85 / I-385 Gateway Interchange",
        domain=InfrastructureDomain.ROADS,
        zone=MunicipalZone.DOWNTOWN_GREENVILLE,
        latitude=34.8432,
        longitude=-82.3168,
        nominal_capacity=145000.0,  # AADT Vehicles / Day
        unit="Vehicles/Day (AADT)",
        current_utilization_pct=94.2,
        bottleneck_risk_tier="CRITICAL",
        agency_owner="SCDOT District 3"
    ),
    "NODE_ROA_02": InfrastructureNode(
        node_id="NODE_ROA_02",
        name="Woodruff Road (SC-146) Commercial Arterial",
        domain=InfrastructureDomain.ROADS,
        zone=MunicipalZone.WOODRUFF_ROAD_COMMERCIAL,
        latitude=34.8214,
        longitude=-82.2740,
        nominal_capacity=42000.0,
        unit="Vehicles/Day (AADT)",
        current_utilization_pct=108.5,
        bottleneck_risk_tier="CRITICAL",
        agency_owner="SCDOT / Greenville County"
    ),
    "NODE_RAI_01": InfrastructureNode(
        node_id="NODE_RAI_01",
        name="Inland Port Greer (Intermodal Rail Hub)",
        domain=InfrastructureDomain.RAILWAYS,
        zone=MunicipalZone.GREER_INLAND_PORT,
        latitude=34.9125,
        longitude=-82.2031,
        nominal_capacity=175000.0,  # Container Lifts / Year
        unit="Container Lifts/Yr",
        current_utilization_pct=88.7,
        bottleneck_risk_tier="HIGH",
        agency_owner="SC Ports Authority / Norfolk Southern"
    ),
    "NODE_AIR_01": InfrastructureNode(
        node_id="NODE_AIR_01",
        name="GSP International Airport & Cargo Apron",
        domain=InfrastructureDomain.AIRPORT,
        zone=MunicipalZone.GSP_AEROSPACE_CORRIDOR,
        latitude=34.8957,
        longitude=-82.2189,
        nominal_capacity=120000.0,  # Air Cargo Tons / Year
        unit="Cargo Tons/Yr",
        current_utilization_pct=82.1,
        bottleneck_risk_tier="MODERATE",
        agency_owner="GSP Airport Authority"
    ),
    "NODE_ELE_01": InfrastructureNode(
        node_id="NODE_ELE_01",
        name="Duke Energy Mauldin/Pelham Substation Hub",
        domain=InfrastructureDomain.ELECTRICITY,
        zone=MunicipalZone.MAULDIN_URBAN_CORE,
        latitude=34.7812,
        longitude=-82.2985,
        nominal_capacity=450.0,  # Megawatts (MW)
        unit="Megawatts (MW Peak)",
        current_utilization_pct=91.8,
        bottleneck_risk_tier="HIGH",
        agency_owner="Duke Energy Carolinas"
    ),
    "NODE_LND_01": InfrastructureNode(
        node_id="NODE_LND_01",
        name="South County Greenfield Expansion Corridor (Simpsonville/Fountain Inn)",
        domain=InfrastructureDomain.LAND_GROWTH,
        zone=MunicipalZone.SIMPSONVILLE_SPRAWL,
        latitude=34.7371,
        longitude=-82.2543,
        nominal_capacity=1200.0,  # New Parcels / Quarter
        unit="Residential Parcels/Qtr",
        current_utilization_pct=118.0,
        bottleneck_risk_tier="CRITICAL",
        agency_owner="Greenville County Planning & GIS"
    ),
    "NODE_TRA_01": InfrastructureNode(
        node_id="NODE_TRA_01",
        name="Prisma Health Swamp Rabbit Trail Network",
        domain=InfrastructureDomain.TRANSIT_TRAILS,
        zone=MunicipalZone.SWAMP_RABBIT_CORRIDOR,
        latitude=34.8690,
        longitude=-82.4150,
        nominal_capacity=750000.0,  # Annual Trail Users
        unit="Annual Trail Trips",
        current_utilization_pct=84.5,
        bottleneck_risk_tier="MODERATE",
        agency_owner="City of Greenville Parks & Rec"
    )
}
