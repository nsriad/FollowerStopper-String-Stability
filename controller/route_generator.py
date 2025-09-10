# controller/route_generator.py
import os

def generate_ring_route(vehicle_types, vehicle_plan, filename="route/ring.rou.xml"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write("<routes>\n")

        # Write vehicle types
        for vtype, attrs in vehicle_types.items():
            f.write(f'  <vType id="{vtype}" carFollowModel="{attrs["carFollowModel"]}" '
                    f'accel="{attrs["accel"]}" decel="{attrs["decel"]}" '
                    f'tau="{attrs["tau"]}" minGap="{attrs["minGap"]}" '
                    f'maxSpeed="{attrs["maxSpeed"]}" guiShape="passenger"/>\n')

        # Use circular edge IDs
        # loop_count = int(2200 / 40) + 2
        # edges = ' '.join(['e0 e1 e2 e3'] * loop_count)
        loop_count =  2  # min. number of loops needed
        single_loop_edges = ' '.join([f"e{i}" for i in range(40)])
        edges = ' '.join([single_loop_edges] * loop_count)

        f.write(f'  <route id="loop" edges="{edges}"/>\n')

        # Compute total number of followers
        num_followers = sum(count for _, count in vehicle_plan)
        num_vehicles = 1 + num_followers  # +1 for leader

        gap = 12  # meters between vehicles

        # Starting position (leader at front)
        start_pos = gap * (num_vehicles - 1)

        # Leader vehicle (veh0)
        f.write(f'  <vehicle id="veh0" type="idm_follower" route="loop" depart="0" departPos="{start_pos}" color="255,0,0"/>\n')

        # Write followers
        # Followers
        veh_id = 1
        for vtype, count in vehicle_plan:
            for i in range(count):
                depart_pos = start_pos - (veh_id * gap)
                r = (0 + 90 * i) % 256
                g = (50 + 60 * i) % 256
                b = (150 + 10 * i) % 256

                f.write(f'  <vehicle id="veh{veh_id}" type="{vtype}" route="loop" '
                        f'depart="0" departPos="{depart_pos}" color="{r},{g},{b}"/>\n')
                veh_id += 1

        f.write("</routes>\n")

    print(f"Route file generated: {filename}")



# for straight road

def generate_straight_route(vehicle_types, vehicle_plan, filename="route/straight.rou.xml"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write("<routes>\n")

        # Write vehicle types
        for vtype, attrs in vehicle_types.items():
            f.write(f'  <vType id="{vtype}" carFollowModel="{attrs["carFollowModel"]}" '
                    f'accel="{attrs["accel"]}" decel="{attrs["decel"]}" '
                    f'tau="{attrs["tau"]}" minGap="{attrs["minGap"]}" '
                    f'maxSpeed="{attrs["maxSpeed"]}" guiShape="passenger"/>\n')

        # Route is the straight edge
        f.write('  <route id="straight" edges="e0"/>\n')

        # Compute total number of followers
        num_followers = sum(count for _, count in vehicle_plan)
        num_vehicles = 1 + num_followers  # +1 for leader

        gap = 12  # meters between vehicles

        # Starting position (leader at front)
        start_pos = gap * (num_vehicles - 1)

        # Leader vehicle (veh0)
        f.write(f'  <vehicle id="veh0" type="idm_follower" route="straight" depart="0" departPos="{start_pos}" color="255,0,0"/>\n')

        # Followers
        veh_id = 1
        for vtype, count in vehicle_plan:
            for i in range(count):
                depart_pos = start_pos - (veh_id * gap)
                r = (0 + 90 * i) % 256
                g = (50 + 60 * i) % 256
                b = (150 + 10 * i) % 256

                f.write(f'  <vehicle id="veh{veh_id}" type="{vtype}" route="straight" '
                        f'depart="0" departPos="{depart_pos}" color="{r},{g},{b}"/>\n')
                veh_id += 1

        f.write("</routes>\n")

    print(f"Route file generated: {filename}")


# for circular road
def generate_circular_road(vehicle_types, vehicle_plan, filename="route/circular.rou.xml"):
    with open(filename, "w") as f:
        f.write("<routes>\n")

        # Write vehicle types
        for vtype, attrs in vehicle_types.items():
            f.write(f'  <vType id="{vtype}" carFollowModel="{attrs["carFollowModel"]}" '
                    f'accel="{attrs["accel"]}" decel="{attrs["decel"]}" '
                    f'tau="{attrs["tau"]}" minGap="{attrs["minGap"]}" '
                    f'maxSpeed="{attrs["maxSpeed"]}" guiShape="passenger"/>\n')

        # Use circular edge IDs
        loop_count = int(2200 / 40) + 2
        edges = ' '.join(['e0 e1 e2 e3'] * loop_count)
        f.write(f'  <route id="loop" edges="{edges}"/>\n')
        # f.write('  <route id="loop" edges="e0 e1 e2 e3 e0"/>\n')
        f.write('  <vehicle id="veh0" type="leader" route="loop" depart="0" color="255,0,0"/>\n')

        # Write followers
        depart_time = 1
        veh_id = 1
        base_color = (0, 50, 100)  # Starting color for followers
        for vtype, count in vehicle_plan:
            for i in range(count):
                # Change the blue channel gradually
                r = (base_color[0] + 10 * i) % 256
                g = (base_color[1] + 60 * i) % 256
                b = (base_color[2] + 110 * i) % 256

                color_str = f"{r},{g},{b}"
                print(color_str)

                f.write(f'  <vehicle id="veh{veh_id}" type="{vtype}" route="loop" depart="{depart_time}" color="{r},{g},{b}"/>\n')
                veh_id += 1
                depart_time += 1

        f.write("</routes>\n")

    print(f"Route file generated: {filename}")