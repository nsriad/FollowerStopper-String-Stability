import matplotlib.pyplot as plt
from matplotlib import rcParams
from controller.controller_manager import get_controller_name
import traci

# Plot styling
rcParams["text.usetex"] = True
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["Times"]
rcParams["font.size"] = 14
rcParams["axes.labelsize"] = 16
rcParams["xtick.labelsize"] = 14
rcParams["ytick.labelsize"] = 14
rcParams["legend.fontsize"] = 14

def plot_speeds(time_log, ref_speed, speeds, cf_models = None, ref_vels = None, del_t = 0.1, save_path=None, xlim_start=None, xlim_end=None, ylim_bottom=None, ylim_top=None):
    plt.figure(figsize=(8, 5))

    # Sort vehicle IDs (e.g., veh0, veh1, veh2, ...)
    sorted_ids = sorted(speeds.keys(), key=lambda vid: int(vid.replace("veh", "")))

    for idx, veh_id in enumerate(sorted_ids):
        speed_list = speeds[veh_id]
        sliced_x = [time_log[i] * del_t for i in range(len(speed_list))]

        if idx == 0:
            label = "Leader"
            linestyle = '-'
            linewidth = 1.5

        elif idx == 1:
            label = "Follower1"
            linestyle = '-'
            linewidth = 1

        else:
            follower_num = idx
            # controller_name = get_controller_name(veh_id) or "default"
            if cf_models and veh_id in cf_models:
                model = cf_models[veh_id]
            else:
                model = "unknown"
            label = f"Follower{follower_num}"
            linestyle = '-'
            linewidth = 1.0

        plt.plot(sliced_x, speed_list, label=label, linestyle=linestyle, linewidth=linewidth)

    # plt.plot(sliced_x, ref_vels['veh1'], label='Reference r', linestyle='--')

    plt.xlabel(r"\textbf{Time (s)}")
    plt.ylabel(r"\textbf{Speed (m/s)}")
    plt.title(r"\textbf{Speed Over Time}")
    plt.legend()
    plt.grid(True)

    # Set x-axis limits
    if xlim_start is not None or xlim_end is not None:
        if xlim_end is None:
            xlim_end = time_log[-1]
        plt.xlim(left=xlim_start, right=xlim_end)

    # Set y-axis limits
    if ylim_bottom is not None or ylim_top is not None:
        plt.ylim(bottom=ylim_bottom, top=ylim_top)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, format='pdf')
        print(f"Plot saved to: {save_path}")
    plt.show()
