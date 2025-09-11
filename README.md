# FollowerStopper String Stability

Simulation framework for evaluating **string stability** in mixed-autonomy traffic using the FollowerStopper controller.  
This project integrates **SUMO** (Simulation of Urban MObility) with Python to analyze wave-dampening performance, headway stability, and autonomous vehicle behaviors across different road network types.

---

## Features
- Supports **multiple network types**: Ring, Straight, and Circular.
- **Mixed-autonomy simulation**: Human-driven and autonomous vehicles in one environment.
- **String stability metrics**: Headway, velocity amplification, spacing error analysis.
- **Customizable parameters**: Reference speed, simulation duration, network topology.
- **Visualization tools**: Automated plots of vehicle speeds and spacing over time.
- **Export utilities**: Saves simulation data in `.csv` and figures in `.pdf` format.

---

## Project Structure
```
FollowerStopper-String-Stability/
│
├── main.py                 # Main entry point for running simulations
├── controller/             # Route generation, vehicle config, simulation logic
├── analysis/               # Plotting scripts and data analysis notebooks
├── figures/                # Auto-generated plots
├── output/                 # Simulation results (CSV files)
├── sumo_config/            # SUMO network and route configuration files
└── requirements.txt        # Python dependencies (to be created)
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nsriad/FollowerStopper-String-Stability.git
cd FollowerStopper-String-Stability
```

### 2. Set up Python Environment
We recommend using Python 3.8+ and `virtualenv`:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install SUMO
- [Download SUMO](https://www.eclipse.org/sumo/) and add it to your system PATH.  
- Ensure `sumo` and `sumo-gui` commands work in your terminal.

---

## Usage

Run a simulation from the project root:
```bash
python main.py
```

Key parameters in `main.py`:
- **network_type**: `ring`, `straight`, or `circular`
- **ref_speed**: Desired reference speed (m/s)
- **interrupt_time**: Simulation duration (seconds)
- **freq**: Sampling frequency (Hz)

Simulation generates:
- **Plots** → `figures/<network_type>/`
- **CSV Data** → `output/<network_type>/`

---

## Example Output

After running:
```bash
python main.py
```

You will find:
- Vehicle speed plots: `figures/<network_type>/...pdf`
- Simulation data: `output/<network_type>/...csv`

---

## Dependencies
To be listed in `requirements.txt`:
```
traci
sumolib
matplotlib
numpy
pandas
```

---

## Citation
Will be added later after publication.
```

---

## License
This project is released under the MIT License.
