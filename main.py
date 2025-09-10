import os
import sys
import traci
import sumolib
from controller.simulation import *
from controller.io_utils import *
from analysis.plot_stability import *
from controller.vehicle_config import *
from controller.route_generator import *

ref_speed = 20
interrupt_time = 500 # in second
freq = 50
del_t = 1/freq
idm_duration = 120 # in second

def main():
    vehicle_plan = [("idm_follower", 7)]

    # Select network type
    network_type = "straight"  # Options: "ring", "straight", "circular"

    if network_type == "ring":
        route_file = "sumo_config/route/ring.rou.xml"
        cfg_file = "sumo_config/config/ring.sumocfg"
        generate_ring_route(vehicle_types, vehicle_plan, filename=route_file)

    elif network_type == "straight":
        route_file = "sumo_config/route/straight.rou.xml"
        cfg_file = "sumo_config/config/straight.sumocfg"
        generate_straight_route(vehicle_types, vehicle_plan, filename=route_file)

    elif network_type == "circular":
        route_file = "sumo_config/route/circular.rou.xml"
        cfg_file = "sumo_config/config/circular.sumocfg"
        generate_straight_route(vehicle_types, vehicle_plan, filename=route_file)

    else:
        raise ValueError(f"Unknown network type: {network_type}")


    # start sumo
    SUMO_BINARY = "sumo-gui"  # "sumo" Or "sumo-gui" for GUI version
    os.makedirs(os.path.dirname(cfg_file), exist_ok=True)
    sumo_cmd = [SUMO_BINARY, "-c", cfg_file, "--step-length", f"{del_t}"]
    traci.start(sumo_cmd)
    
    #reference speed
    global ref_speed

    # Get all recorded simulation data
    time_log, speeds, accelerations, x_positions, y_positions, headways, cf_models, ref_vels = run_simulation(ref_speed, interrupt_time, freq, idm_duration)


    n_followers = len(speeds) - 1 # number of followers
    plot_path = f"figures/{network_type}/04092025_latest_09042025_{freq}_IDM_FS_followers_{n_followers}.pdf"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    csv_path = f"output/{network_type}/04092025_latest_{freq}_IDM_FS_followers_{n_followers}.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # Save full simulation data to CSV
    save_simulation_to_csv(
        time_log, speeds, accelerations, x_positions, y_positions, headways, ref_vels,
        save_path=csv_path
    )
    plot_speeds(time_log, ref_speed, speeds, cf_models=cf_models, ref_vels = ref_vels, del_t = del_t, save_path=plot_path, xlim_start=0, xlim_end=200, ylim_bottom=None, ylim_top=None)

if __name__ == "__main__":
    main()
