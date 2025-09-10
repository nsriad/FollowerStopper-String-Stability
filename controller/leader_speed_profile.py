# controller/leader_profile.py
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
# Plot styling
rcParams["text.usetex"] = True
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["Times"]
rcParams["font.size"] = 14
rcParams["axes.labelsize"] = 16
rcParams["xtick.labelsize"] = 14
rcParams["ytick.labelsize"] = 14
rcParams["legend.fontsize"] = 14

_speed_profile = []
_time_profile = []

import matplotlib.pyplot as plt

_speed_profile = []
_time_profile = []

def load_real_profile(csv_path, freq):
    global _speed_profile, _time_profile

    df = pd.read_csv(csv_path)

    # Use first column as POSIX timestamps (in seconds with microseconds)
    time_col = df.columns[0]
    speed_col = 'Message'

    # Replace missing speed values with 0
    df[speed_col] = df[speed_col].fillna(0)

    # Skip leading zero speeds
    start_idx = next((i for i, s in enumerate(df[speed_col]) if s > 0), 0)
    df = df.iloc[start_idx:].reset_index(drop=True)

    # Convert speed from km/h to m/s
    df[speed_col] = df[speed_col] * (1000 / 3600)

    # Convert POSIX time to relative time in seconds
    start_time = df[time_col].iloc[0]
    df['timestamp'] = df[time_col] - start_time  # already in seconds

    # # KEEP ORIGINAL SAMPLING
    # _speed_profile = df[speed_col].to_numpy()
    # _time_profile = df['timestamp'].to_numpy()

    # Resample to fixed 0.1s steps
    max_time = df['timestamp'].iloc[-1]
    ts_uniform = np.arange(0, max_time, 1/freq)  # uniform resolution
    speed_uniform = np.interp(ts_uniform, df['timestamp'], df[speed_col])

    # Store values
    _speed_profile = speed_uniform     # in m/s


    # Plot the result
    # plt.figure(figsize=(12, 5))
    # plt.plot(_time_profile, _speed_profile, label="Original Leader Speed", color="blue")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Speed (m/s)")
    # plt.title("Real-World Speed Profile Over Time")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()


def real_profile(step):
    return _speed_profile[step] if step < len(_speed_profile) else 0.0

def get_profile_length():
    # print  (f"Leader profile length: {len(_speed_profile)}")
    return len(_speed_profile)

def stop_and_go_profile(step):
    """
    Sinusoidal stop-and-go speed profile.
    Varies between 5 and 25 m/s over time.
    """
    speed = 15 + 10 * math.sin(2 * math.pi * step / 100)
    return max(2, speed)

def step_profile(step):
    if 30 <= step < 50:
        return 10.0
    return 25.0

def constant_speed():
    return 25.0


# def load_real_profile(csv_path):
#     global _speed_profile

#     df = pd.read_csv(csv_path)

#     # 
#     speed_col = 'Message'
#     raw_speeds = df[speed_col].fillna(0).tolist()

#     # Find the index of the first non-zero speed
#     start_idx = next((i for i, s in enumerate(raw_speeds) if s > 0), 0)

#     # Trim and convert to m/s
#     _speed_profile = [s * 1 for s in raw_speeds[start_idx:]]

def real_profile(step):
    if step < len(_speed_profile):
        return _speed_profile[step]
    return 0.0
