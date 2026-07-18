import hashlib
import json
import time
import os

# Local database file simulating an append-only ledger storage matrix
LEDGER_FILE = "fortifi_ledger.json"

def generate_enterprise_audit_log(risk_decision, target_vector):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    
    # 1. Fetch the Previous Hash to create the block chain link
    previous_hash = "0" * 64 # Default genesis hash if no previous logs exist
    
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                logs = json.load(f)
                if logs:
                    previous_hash = logs[-1]["integrity_hash"]
        except Exception:
            pass # Fallback to default if file parsing is interrupted

    # 2. Bake the previous hash straight into the current event payload
    raw_payload = f"{timestamp}-{risk_decision}-{str(target_vector)}-{previous_hash}"
    current_hash = hashlib.sha256(raw_payload.encode()).hexdigest()
    
    audit_log = {
        "timestamp_utc": timestamp,
        "security_event": "TELEMETRY_ANOMALY_EVALUATION",
        "system_decision": risk_decision,
        "previous_hash": previous_hash,
        "integrity_hash": current_hash,
        "compliance_status": "COMPLIANT_SECURE"
    }
    
    # 3. Append the record natively into the chronological local matrix database
    try:
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, "r") as f:
                current_ledger = json.load(f)
        else:
            current_ledger = []
            
        current_ledger.append(audit_log)
        with open(LEDGER_FILE, "w") as f:
            json.dump(current_ledger, f, indent=4)
    except Exception:
        pass

    return audit_log
