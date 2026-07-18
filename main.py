from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List
import numpy as np
import analytics
import security

app = FastAPI(title="FortiFi Enterprise Threat Analytics API", version="2.1")

# 1. Define the Cryptographically Secure Access Parameters
API_KEY = "fortifi_secret_sovereign_token_2026"
API_KEY_NAME = "X-FortiFi-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(header_value: str = Depends(api_key_header)):
    if header_value == API_KEY:
        return header_value
    raise HTTPException(status_code=401, detail="Unauthorized Access: Invalid or Missing FortiFi API Key Header.")

# Data Ingestion Validation Schema using Pydantic
class CoordinateNode(BaseModel):
    x: float
    y: float
    z: float

class TelemetryPayload(BaseModel):
    target_id: str
    coordinates: List[CoordinateNode]

@app.get("/")
async def root():
    return {"status": "ONLINE", "system": "FORTIFI CORE ENGINE V2.1"}

# 2. Hardened REST Endpoint protected by API Key Security Headers
@app.post("/api/v2/telemetry")
async def process_telemetry_stream(payload: TelemetryPayload, authenticated: str = Depends(validate_api_key)):
    if len(payload.coordinates) < 4:
        raise HTTPException(status_code=400, detail="Insufficient nodes. Minimum 4 spatial coordinates required.")
        
    coord_matrix = np.array([[node.x, node.y, node.z] for node in payload.coordinates])
    
    pos_t0, pos_t1, pos_t2, pos_t3 = coord_matrix, coord_matrix, coord_matrix, coord_matrix
    
    vel_v1 = pos_t1 - pos_t0
    vel_v2 = pos_t2 - pos_t1
    vel_v3 = pos_t3 - pos_t2
    
    acc_a1 = vel_v2 - vel_v1
    acc_a2 = vel_v3 - vel_v2
    
    jerk_vector = acc_a2 - acc_a1
    absolute_jerk = np.linalg.norm(jerk_vector)
    
    if absolute_jerk > 4.0:
        decision = "🔴 CRITICAL TARGET ANOMALY: HIGH JERK PROFILE DETECTED. ENFORCING AUTOMATED OVERRIDE BLOCK."
    else:
        decision = "🟢 LOW RISK SYSTEM INTEGRITY: ENVIRONMENT NOISE COMPLIANT."
        
    audit_record = security.generate_enterprise_audit_log(decision, [payload.target_id])
    
    return {
        "target_id": payload.target_id,
        "absolute_jerk_magnitude": round(float(absolute_jerk), 2),
        "system_assessment": decision,
        "security_ledger_signature": audit_record["integrity_hash"]
    }
