import traci
import math
import numpy as np

# Keep this persistent across time steps
_nominal_y = 0.0

def nominal_controller(vel, max_speed, max_accel, max_decel, freq):
    """
    Nominal controller to generate reference velocity r.
    This smooths acceleration/deceleration over time.
    
    Inputs:
    - vel: current vehicle speed (v_AV)
    - max_speed: desired target speed from user
    - max_accel: maximum allowable acceleration
    - max_decel: maximum allowable deceleration (positive value)
    - dt: time step (should match simulation step, e.g., 0.1s)
    
    Returns:
    - r: reference speed (to be used as input to the FollowerStopper controller)
    """
    global _nominal_y
    dt = 1/freq

    if _nominal_y > max_speed + 1:
        _nominal_y = max(max_speed, _nominal_y - abs(max_decel) * dt)
    elif _nominal_y < max_speed - 1:
        _nominal_y = min(max_speed, _nominal_y + max_accel * dt)
    else:
        _nominal_y = float(max_speed)

    # rounding
    if _nominal_y < 2 and max_speed > 2:
        _nominal_y = 2
    elif _nominal_y < 1 and max_speed > 1:
        _nominal_y = 1

    # Output bounded reference
    r = min(max(_nominal_y, vel - 1.0), vel + 2.0)
    return r


def follower_stopper(r, dx, dv, v_AV, dx_min, dx_activate, decel, h):
    """
    Safety controller using quadratic bands.
    
    Parameters:
        r          : desired velocity (from other models)
        dx         : estimated gap to vehicle ahead
        dv         : estimated dẋ (i.e., lead - ego speed)
        v_AV       : velocity of the ego (autonomous) vehicle
        dx_min     : minimum spacing (omega_1)
        dx_activate: activation spacing (omega_3)
        decel      : list or array of 3 deceleration values for parabolas

    Returns:
        u_cmd: commanded velocity (always <= r)
    """

    # Controller-specific spacing mid point
    dx_mid = (dx_min + dx_activate) / 2.0

    # Estimate lead vehicle speed
    v_lead = v_AV + dv
    v_lead = max(v_lead, 0.0)  # Lead vehicle cannot go backward
    v = min(r, v_lead)       # Desired velocity cannot exceed safe lead speed

    # Ensure dv is non-negative for band calculation
    dv = min(dv, 0.0)

    # Band boundary calculations
    dx1 = dx_min + (1 / (2 * decel[0])) * dv**2 #+ v_AV*h[0]
    dx2 = dx_mid + (1 / (2 * decel[1])) * dv**2 #+ v_AV*h[1]
    dx3 = dx_activate + (1 / (2 * decel[2])) * dv**2 #+ v_AV*h[2]

    # Compute u_cmd based on parabolic interpolation
    if dx < dx1:
        u_cmd = 0.0
    elif dx1 <= dx < dx2:
        u_cmd = v * (dx - dx1) / (dx2 - dx1) #adaptation region between x1 and x2
    elif dx2 <= dx < dx3:
        u_cmd = v + (r - v) * (dx - dx2) / (dx3 - dx2) #adaptation region between x2 and x3
    else:
        u_cmd = r

    return u_cmd


# Simple Gap-Based Speed Controller 
def simple_gap_controller(veh_id, Kp=0.4, desired_gap=5.0):
    leader_info = traci.vehicle.getLeader(veh_id)
    if not leader_info or leader_info[0] == "":
        return traci.vehicle.getSpeed(veh_id)

    leader_id, gap = leader_info
    follower_speed = traci.vehicle.getSpeed(veh_id)

    error = gap - desired_gap
    new_speed = follower_speed + Kp * error

    return max(0, min(new_speed, 30))


# Acceleration-Based Controller
def accel_based_controller(veh_id, desired_gap=5.0, Kp=0.3, max_acc=2.5, max_dec=4.5):
    leader_info = traci.vehicle.getLeader(veh_id)
    if not leader_info or leader_info[0] == "":
        return

    leader_id, gap = leader_info
    leader_speed = traci.vehicle.getSpeed(leader_id)
    follower_speed = traci.vehicle.getSpeed(veh_id)

    gap_error = gap - desired_gap
    speed_error = leader_speed - follower_speed

    accel = max_acc * math.tanh(Kp * gap_error + 0.2 * speed_error)
    accel = max(-max_dec, min(accel, max_acc))

    return accel


# Controller Map
controller_map = {
    "simple_gap": simple_gap_controller,
    "accel_based": accel_based_controller
}

# Default Controller (global for all followers)
default_controller = None  # e.g., "accel_based"

# Per-Vehicle Custom Controller Assignment
controller_assignment = {
    "veh1": "simple_gap",
    "veh2": "accel_based"
}


# --- Dispatcher Logic ---
def get_controller_name(veh_id):
    return controller_assignment.get(veh_id, default_controller)

def apply_controller(veh_id):
    controller_name = get_controller_name(veh_id)
    if not controller_name:
        return  # No controller specified

    func = controller_map.get(controller_name)
    if not func:
        return  # Invalid controller

    if controller_name == "accel_based":
        accel = func(veh_id)
        if accel is not None:
            traci.vehicle.setAcceleration(veh_id, accel, duration=1.0)
            print("Acceleration based controller applied")
    else:
        speed = func(veh_id)
        if speed is not None:
            traci.vehicle.setSpeed(veh_id, speed)
            print("Gap based controller applied")

