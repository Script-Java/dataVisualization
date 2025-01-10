from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import NamedTuple
import pypsa

start_timestamp = datetime.fromisoformat("2024-04-11T00:00:00Z")
snapshots = [start_timestamp + timedelta(hours=h) for h in range(24)]
wind_profile = pd.Series(
    {snapshot: np.exp((snapshot.hour - 23)/24) for snapshot in snapshots})
ld1_profile = pd.Series({snapshot: 0.13 * snapshot.hour/8 + 0.01 if snapshot.hour < 8 else 0.26 *
                        snapshot.hour/5 if snapshot.hour < 20 else 0.14 * snapshot.hour/24 for snapshot in snapshots})
ld2_profile = pd.Series({snapshot: 0.10 * snapshot.hour/8 + 0.01 if snapshot.hour < 8 else 0.34 * snapshot.hour/7 if snapshot.hour < 20
                         else 0.12 * snapshot.hour/24 for snapshot in snapshots})
# Build network
network = pypsa.Network(snapshots=wind_profile.index)


class Coordinate(NamedTuple):
    x: float
    y: float


coordinate_by_bus_label = {"1": Coordinate(x=0, y=0),
                           "2": Coordinate(x=-2, y=3),
                           "3": Coordinate(x=2, y=3),
                           "4": Coordinate(x=0, y=1),
                           "5": Coordinate(x=-1, y=2),
                           "6": Coordinate(x=1, y=2),
                           "7": Coordinate(x=-1, y=3),
                           "8": Coordinate(x=0, y=3),
                           "9": Coordinate(x=1, y=3)}

for bus_label, coordinate in coordinate_by_bus_label.items():
    network.add("Bus", name=bus_label, x=coordinate.x, y=coordinate.y)

lines_data = {
    "line_name": ["ln4-5", "ln4-6", "ln6-9", "ln5-7", "ln7-8", "ln8-9"],
    "bus0": ["4", "4", "6", "5", "7", "8"],
    "bus1": ["5", "6", "9", "7", "8", "9"],
    "r": [0.17, 0.039, 0.019, 0.039, 0.0085, 0.032],
    "x": [0.092, 0.17, 0.1008, 0.072, 0.161, 0.085],
}

for i in range(len(lines_data["line_name"])):
    network.add("Line",
                lines_data["line_name"][i],
                bus0=lines_data["bus0"][i],
                bus1=lines_data["bus1"][i],
                r=lines_data["r"][i],
                x=lines_data["x"][i],
                s_nom=1000)

transformers_data = {
    "transformer_name": ["xf1-4", "xf2-7", "xf9-3"],
    "bus0": ["1", "2", "9"],
    "bus1": ["4", "7", "3"],
    "r": [0.001, 0.001, 0.001],
    "x": [0.0576, 0.0586, 0.0625],
}

for i in range(len(transformers_data["transformer_name"])):
    network.add("Transformer",
                transformers_data["transformer_name"][i],
                bus0=transformers_data["bus0"][i],
                bus1=transformers_data["bus1"][i],
                r=transformers_data["r"][i],
                x=transformers_data["x"][i],
                model="pi",
                s_nom=1000)

# Add loads
network.add("Load", f"ld1", bus="5", p_set=165 * ld1_profile)
network.add("Load", f"ld2", bus="6", p_set=165 * ld2_profile)

# Add generators
network.add("Generator", f"Gn1", bus="1", control="slack",
            committable=True, carrier="nuclear", p_nom=4000.0, marginal_cost=10.0)
network.add("Generator", f"Gn2", bus="2", committable=True,
            carrier="gas", p_nom=2000.0, marginal_cost=50.0)
network.add("Generator", f"Gn3", bus="3", committable=True,
            carrier="wind", p_nom=1000.0, marginal_cost=0.0, p_max_pu=wind_profile)
network.plot()

#network.optimize.optimize_security_constrained(
#    snapshots=snapshots, branch_outages=network.lines.index[:6], solver_name="cbc")

#ax = network.lines_t['p0']['ln4-5'].plot(style='bo-')
#network.loads_t['p_set']['ld1'].plot(ax=ax, style='rx-')
#ax.grid(True)

# produce static data files
network.buses.to_csv("static_buses.csv")
network.lines.to_csv("static_lines.csv")
network.transformers.to_csv("static_transformers.csv")
network.generators.to_csv("static_generators.csv")
network.loads.to_csv("static_loads.csv")
network.buses_t['p'].to_csv("buses_injection_timeseries.csv")
network.generators_t['p'].to_csv("generation_production_timeseries.csv")
network.lines_t['p0'].to_csv("lines_from_timeseries.csv")
network.transformers_t['p0'].to_csv("transformers_from_timeseries.csv")