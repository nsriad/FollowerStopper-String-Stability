import os
import pandas as pd

def save_simulation_to_csv(time_log, speeds, accelerations, x_positions, y_positions, headways, ref_vels, save_path="output/simulation.csv"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    records = []
    sorted_ids = sorted(speeds.keys())

    for t_idx, time in enumerate(time_log):
        for i, vid in enumerate(sorted_ids):
            role = "Leader" if i == 0 else f"Follower{i}"
            
            if t_idx < len(speeds[vid]):
                records.append({
                    "time_step": time,
                    "vehicle_id": vid,
                    "role": role,
                    "speed_mps": speeds[vid][t_idx],
                    "acceleration": accelerations[vid][t_idx],
                    "x": x_positions[vid][t_idx],
                    "y": y_positions[vid][t_idx],
                    "space_headway": headways[vid][t_idx],
                    "ref_vels": ref_vels[vid][t_idx] if vid in ref_vels and t_idx < len(ref_vels[vid]) else None
                })

    df = pd.DataFrame(records)
    df.to_csv(save_path, index=False)
    # print(f"Simulation CSV saved to: {save_path}")
