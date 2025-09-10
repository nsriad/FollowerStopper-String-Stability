import traci
from collections import defaultdict
from controller.controller_manager import *
from controller.vehicle_config import vehicle_types
from controller.leader_speed_profile import *

def run_simulation(ref_speed, interrupt_time, freq, idm_duration):
    step = 0
    traci.simulationStep()  # Trigger vehicle spawn

    vehicle_ids = traci.vehicle.getIDList()
    if not vehicle_ids:
        raise RuntimeError("No vehicles found in simulation. Check route file.")

    leader_id = sorted(vehicle_ids)[0] #veh0
    traci.vehicle.setSpeedMode(leader_id, 0) #disable sumo driving model
    # print("Leader ID: ", leader_id)
    # reset first follower driving mode
    # first_follower_id = sorted(vehicle_ids)[1] #veh1
    # traci.vehicle.setSpeedMode(first_follower_id, 0)

    # for vid in vehicle_ids:
    #     traci.vehicle.setSpeedMode(vid, 0)
    #     print(f"vehicle {vid} is disabled for default mode")

    time_log = []

    speeds = defaultdict(list)
    x_positions = defaultdict(list)
    y_positions = defaultdict(list)
    accelerations = defaultdict(list)
    headways = defaultdict(list)
    ref_vels = defaultdict(list)  # To store r per follower_id
    vehicle_cf_model = {}

    leader_speed_list = []

    # Load leader speed profile
    load_real_profile("controller/2021-07-26-21-10-20_2T3H1RFV8LC057037_CAN_Messages_decoded_speed.csv", freq)

    while True:
        traci.simulationStep()
        current_ids = traci.vehicle.getIDList()

        if len(current_ids) > 1:
            first_follower_id = sorted(current_ids)[1] #veh1
            # print("First Follower ID: ", first_follower_id)
        else:
            first_follower_id = None


        # Skip if no vehicles left
        if not current_ids:
            print("All vehicles have exited.")
            break

        follower_ids = [vid for vid in current_ids if vid != leader_id]

        # Apply leader speed if profile still has data
        if step < get_profile_length():
            if leader_id in current_ids:
                leader_speed = real_profile(step)
                # print(f"Step {step}, Leader speed = {leader_speed} m/s")
                traci.vehicle.setSpeed(leader_id, leader_speed)
                if step < idm_duration*freq:
                    leader_speed_list.append(leader_speed)

                else:
                    if step == idm_duration*freq:
                        # At switch point: calculate average of last 200 from phase 1
                        last_200 = leader_speed_list[-200:] if len(leader_speed_list) >= 200 else leader_speed_list
                        ref_speed = sum(last_200) / len(last_200)
                        print(f"Initial ref_speed from last 200 steps of IDM phase: {ref_speed:.2f} m/s")

                        #reset all other driving mode to run FS controller
                        for vid in vehicle_ids:
                            traci.vehicle.setSpeedMode(vid, 0)
                            print(f"vehicle {vid} is disabled for default mode")

                        # Replace leader_speed_list with only last 200
                        leader_speed_list = last_200.copy()

                    # add latest leader speed to rolling list
                    leader_speed_list.append(leader_speed)
                    if len(leader_speed_list) > 200:
                        leader_speed_list.pop(0)  # keep only last 200

                    # Compute rolling average
                    ref_speed = sum(leader_speed_list) / len(leader_speed_list)

                    #apply nominal and FS controller to AV which is first follower
                    for follower_id in follower_ids:
                        gap_info = traci.vehicle.getLeader(follower_id, 2000) # find leader within 2 km ahead
                        if gap_info:
                            dx = gap_info[1]
                            v_av = traci.vehicle.getSpeed(follower_id)
                            v_lead = traci.vehicle.getSpeed(gap_info[0])
                            dv = v_lead - v_av
                            dx_min = 4.5 # omega_1
                            dx_activate = 6.0 # omega 3
                            decel = [1.5, 1.0, 0.5]
                            h = [0.4, 1.2, 1.8]
                            
                            # applying nominal controller
                            # r = nominal_controller(
                            #     vel = v_av,
                            #     max_speed = ref_speed, # desired cruising speed
                            #     max_accel = 2.0,
                            #     max_decel = -2.0,
                            #     freq = freq
                            # )

                            r = ref_speed
                            
                            r = round(r, 4)  # Round to 4 decimal places
                            # print(f"New r = {r}")

                            ref_vels[follower_id].append(r)

                            u_cmd = follower_stopper(r, dx, dv, v_av, dx_min, dx_activate, decel, h)
                            traci.vehicle.setSpeed(follower_id, u_cmd)
                        else:
                            print(f"At step: {step}, No leader found!!")

        else:
            # Leader profile finished
            if leader_id in current_ids:
                # Optional: stop the leader or let it coast
                #traci.vehicle.setSpeed(leader_id, 0.0)
                break
            if not follower_ids:
                print(f"Leader profile finished and all followers exited at step {step}. Ending simulation.")
                break
            else:
                print(f"Leader profile finished at step {step}, waiting for {len(follower_ids)} followers.")
                break

        # Record speed and position data
        for vid in current_ids:
            speed = round(traci.vehicle.getSpeed(vid), 4)
            acc = round(traci.vehicle.getAcceleration(vid), 4)
            x, y = traci.vehicle.getPosition(vid)
            x = round(x, 4)
            y = round(y, 4)

            speeds[vid].append(speed)
            accelerations[vid].append(acc)
            x_positions[vid].append(x)
            y_positions[vid].append(y)

            leader_info = traci.vehicle.getLeader(vid)
            headway = round(leader_info[1], 4) if leader_info else float('nan')
            # print(f"Step: {step}, Vehicle: {vid}, headway: {headway}")
            headways[vid].append(headway)

            if step < idm_duration * freq:
                ref_vels[vid].append(float('nan'))

            if vid not in vehicle_cf_model:
                try:
                    vtype = traci.vehicle.getTypeID(vid)
                    cf_model = vehicle_types.get(vtype, {}).get("carFollowModel", "unknown")
                    vehicle_cf_model[vid] = cf_model
                except:
                    vehicle_cf_model[vid] = "unknown"

        time_log.append(step)
        step += 1

        if(step==interrupt_time*freq):
            return time_log, speeds, accelerations, x_positions, y_positions, headways, vehicle_cf_model, ref_vels

    traci.close()

    print(vehicle_cf_model)
    return time_log, speeds, accelerations, x_positions, y_positions, headways, vehicle_cf_model, ref_vels
