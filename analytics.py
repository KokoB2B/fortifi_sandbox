import numpy as np

def calculate_threat_anomalies():
    pos_t0 = np.array([100.0, 50.0, 300.0])
    pos_t1 = np.array([125.0, 62.0, 305.0])
    pos_t2 = np.array([160.0, 80.0, 312.0])
    
    vel_v1 = pos_t1 - pos_t0
    vel_v2 = pos_t2 - pos_t1
    
    acceleration_vector = vel_v2 - vel_v1
    absolute_acceleration = np.linalg.norm(acceleration_vector)
    
    if absolute_acceleration > 5.0:
        return "🔴 CRITICAL ANOMALY DETECTED"
    return "🟢 LOW RISK"

if __name__ == "__main__":
    calculate_threat_anomalies()
