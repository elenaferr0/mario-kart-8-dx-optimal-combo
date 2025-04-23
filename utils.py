import pandas as pd
import matplotlib.pyplot as plt

speed_headers = ["GroundSpeed", "WaterSpeed", "AirSpeed", "Anti-GravitySpeed"]
handling_headers = ["GroundHandling", "WaterHandling", "AirHandling", "Anti-GravityHandling"]

stats_headers = [*speed_headers, "Acceleration", "Weight", *handling_headers, "Off-RoadTraction", "Mini-Turbo",
                 "Invincibility", "On-RoadTraction"]


def load_aggregated(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    grouped = df.groupby(stats_headers).agg(
        Names=("Name", lambda x: ','.join(x.astype(str))),
        Images=("ImageURL", lambda x: ','.join(x.astype(str))),
    ).reset_index()

    grouped['Speed'] = grouped[speed_headers].sum(axis=1)
    grouped['Handling'] = grouped[handling_headers].sum(axis=1)
    grouped['Stats'] = grouped[stats_headers].sum(axis=1)
    return grouped


def is_dominated(point_x: float, point_y: float, others: pd.DataFrame, x: str, y: str) -> bool:
    dominated = (
            (others[x] >= point_x) & (others[y] >= point_y)
            & ((others[x] > point_x) | (others[y] > point_y))
    )

    return dominated.any()


def plot_pareto_optimal(df: pd.DataFrame, x_label: str, y_label: str):
    pareto_optimals = {}

    pareto_optimal_speed = []
    pareto_optimal_acc = []

    non_pareto_optimal_speed = []
    non_pareto_optimal_acc = []

    print("Pareto optimal points:")
    for i, row in df.iterrows():
        x = row[x_label]
        y = row[y_label]

        others = df[df.index != i]
        if is_dominated(x, y, others, x_label, y_label):
            non_pareto_optimal_speed.append(x)
            non_pareto_optimal_acc.append(y)
            print(f"Dominated: {row['Names']} ({x_label}: {x}, {y_label}: {y})")
            pareto_optimals[row['Names']] = {
                "x": {
                    "field_name": x_label,
                    "value": x,
                },
                "y": {
                    "field_name": y_label,
                    "value": y,
                },
                "url": row['Images'],
            }
        else:
            pareto_optimal_speed.append(x)
            pareto_optimal_acc.append(y)
            print(f"Optimal: {row['Names']} ({x_label}: {x}, {y_label}: {y})")

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.scatter(non_pareto_optimal_speed, non_pareto_optimal_acc, c='blue', alpha=0.5, label='Non-Pareto Optimal')
    plt.scatter(pareto_optimal_speed, pareto_optimal_acc, c='red', label='Pareto Optimal')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f'{x_label} vs {y_label} of Drivers')
    plt.grid(True)
    plt.legend()  # Add a legend to distinguish the colors
    plt.savefig(f'outputs/{x_label}_{y_label}.png')
    plt.show()
    plt.close()
    return pareto_optimals
