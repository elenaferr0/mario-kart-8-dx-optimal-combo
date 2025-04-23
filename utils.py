import pandas as pd
import matplotlib.pyplot as plt
from typing import List

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


def is_dominated(point: List[float], others: pd.DataFrame, labels: List[str]) -> bool:
    # A point is dominated if there exists another point that is:
    # 1. At least as good in all dimensions
    # 2. Strictly better in at least one dimension

    # Initialize a mask for all rows in others
    dominated_mask = pd.Series(True, index=others.index)

    # Check condition 1: At least as good in all dimensions
    for i, label in enumerate(labels):
        dominated_mask &= (others[label] >= point[i])

    # If no points satisfy condition 1, return False
    if not dominated_mask.any():
        return False

    # Check condition 2: Strictly better in at least one dimension
    strictly_better = pd.Series(False, index=others.index)
    for i, label in enumerate(labels):
        strictly_better |= (others[label] > point[i])

    # Combine conditions 1 and 2
    dominated = (dominated_mask & strictly_better)

    return dominated.any()


def find_pareto_optimal(df: pd.DataFrame, labels: List[str], subject: str):
    solution = {
        "dominated": [],
        "optimal": [],
    }

    pareto_optimal = []
    pareto_dominated = []

    for i, row in df.iterrows():
        point = row[labels]  # point in n-th dimensional space

        others = df[df.index != i]
        dominated = is_dominated(point, others, labels)
        if dominated:
            pareto_dominated.append(point)
            print(f"Dominated: {row.Names} ({zip(labels, point)})")
        else:
            pareto_optimal.append(point)

        category = "dominated" if dominated else "optimal"
        solution[category].append({"name": row.Names, "url": row.Images })

    if len(pareto_optimal) == 0:
        print("No Pareto optimal solutions found.")
        return None

    if len(labels) > 3:
        print(f"Not plotting solution as it has {len(labels)} dimensions.")
        return solution

    # Plotting
    if len(labels) == 2:
        # 2D plotting
        x_label, y_label = labels
        plt.figure(figsize=(8, 6))

        # Convert lists to appropriate arrays for plotting
        non_pareto_x = [point[0] for point in pareto_dominated]
        non_pareto_y = [point[1] for point in pareto_dominated]
        pareto_x = [point[0] for point in pareto_optimal]
        pareto_y = [point[1] for point in pareto_optimal]

        plt.scatter(non_pareto_x, non_pareto_y, c='blue', alpha=0.5, label='Non-Pareto Optimal')
        plt.scatter(pareto_x, pareto_y, c='red', label='Pareto Optimal')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f'{x_label} vs {y_label} of {subject}')
        plt.grid(True)
        plt.legend()
        plt.savefig(f'results/plots/{subject}_{x_label}_{y_label}.png')
        plt.close()
    elif len(labels) == 3:
        # 3D plotting
        x_label, y_label, z_label = labels
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Convert lists to appropriate arrays for plotting
        non_pareto_x = [point[0] for point in pareto_dominated]
        non_pareto_y = [point[1] for point in pareto_dominated]
        non_pareto_z = [point[2] for point in pareto_dominated]
        pareto_x = [point[0] for point in pareto_optimal]
        pareto_y = [point[1] for point in pareto_optimal]
        pareto_z = [point[2] for point in pareto_optimal]

        ax.scatter(non_pareto_x, non_pareto_y, non_pareto_z, c='blue', alpha=0.5, label='Non-Pareto Optimal')
        ax.scatter(pareto_x, pareto_y, pareto_z, c='red', label='Pareto Optimal')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        ax.set_title(f'{x_label} vs {y_label} vs {z_label} of {subject}')
        ax.legend()
        plt.savefig(f'results/plots/{subject}_{x_label}_{y_label}_{z_label}.png')
        plt.close()

    return solution
