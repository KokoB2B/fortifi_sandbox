import os
import sys
import json
import time

def run_risk_matrix(coordinate_set, text_stream):
    """
    Executes FortiFi's 3-Tier Risk Decision Matrix over raw telemetry.
    🟢 Low: Allow | 🟡 Medium: Challenge | 🔴 High: Block
    """
    print("\n--- FORTIFI SENTINEL INBOUND SCANNER ACTIVE ---")
    
    # Simulating 3-Tier Data Sanitization & Anomaly Filtering
    x, y, z = coordinate_set
    print(f"[*] Ingesting All-Domain Telemetry Coordinates: X={x}, Y={y}, Z={z}")
    
    # Engine B: Normalized Data Mapping (Regional Slang Context)
    dialect_dictionary = {"klk": "what's up", "vaina": "thing", "tigueraje": "hustle"}
    cleaned_text = " ".join([dialect_dictionary.get(word.lower(), word) for word in text_stream.split()])
    print(f"[*] Engine B Pipeline Output (Normalized text): '{cleaned_text}'")
    
    # Evaluating Threshold Limits (Simulating Target Velocity / Anomaly Flags)
    if abs(x) > 100 or abs(y) > 100 or "block_vector" in cleaned_text:
        risk_level = "🔴 HIGH RISK: CRITICAL THREAT DETECTED. ENFORCING AUTOMATIC OVERRIDE BLOCK."
    elif abs(z) > 50 or "challenge" in cleaned_text:
        risk_level = "🟡 MEDIUM RISK: ANOMALY FLAGGED. DEPLOYING INTERCEPT CHALLENGE ROUTE."
    else:
        risk_level = "🟢 LOW RISK: INTEGRITY VERIFIED. SYSTEM PROCEEDING NORMAL."
        
    print(f"\n[DECISION MATRIX RESULT] -> {risk_level}\n")
    return risk_level

if __name__ == "__main__":
    # Test Data Set 1: Simulated High-Speed Incoming Telemetry Arrays
    mock_coordinates = (142.5, -22.4, 12.0)
    mock_input_text = "System alert code checking variable vaina for threat signatures"
    
    run_risk_matrix(mock_coordinates, mock_input_text)
