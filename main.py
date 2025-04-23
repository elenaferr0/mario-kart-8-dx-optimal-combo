import os, json
from typing import Dict
import pandas as pd
from docplex.mp.model import Model
from utils import load_aggregated, plot_pareto_optimal
import matplotlib.pyplot as plt


def setup_model(m: Model,
                mapper,
                drivers: pd.DataFrame, bodies: pd.DataFrame, tires: pd.DataFrame,
                gliders: pd.DataFrame) -> Model:
    driver_names = drivers.Names
    body_names = bodies.Names
    tire_names = tires.Names
    glider_names = gliders.Names

    # Create decision variables
    d = {i: m.binary_var(name=f'd({i})') for i in driver_names}
    b = {i: m.binary_var(name=f'b({i})') for i in body_names}
    t = {i: m.binary_var(name=f't({i})') for i in tire_names}
    g = {i: m.binary_var(name=f'g({i})') for i in glider_names}

    # Constraints (there can be at most one1 of each type)
    m.add_constraint(m.sum(d[i] for i in driver_names) <= 1, 'one_driver')
    m.add_constraint(m.sum(b[i] for i in body_names) <= 1, 'one_body')
    m.add_constraint(m.sum(t[i] for i in tire_names) <= 1, 'one_tire')
    m.add_constraint(m.sum(g[i] for i in glider_names) <= 1, 'one_glider')

    # Maximize the total score
    driver_score = m.sum(d[driver.Names] * mapper(driver) for i, driver in drivers.iterrows())
    body_score = m.sum(b[body.Names] * mapper(body) for i, body in bodies.iterrows())
    tire_score = m.sum(t[tire.Names] * mapper(tire) for i, tire in tires.iterrows())
    glider_score = m.sum(g[glider.Names] * mapper(glider) for i, glider in gliders.iterrows())

    m.maximize(driver_score + body_score + tire_score + glider_score)
    return m


def extract_solution(m: Model, problem: str, drivers: pd.DataFrame, bodies: pd.DataFrame,
                     tires: pd.DataFrame, gliders: pd.DataFrame) -> Dict:
    sln = {}
    obj = m.objective_value
    print(f"{problem}, Objective value: {obj}")

    print("Optimal solution:")
    selected_drivers = \
        [driver for i, driver in drivers.iterrows() if m.get_var_by_name(f'd({driver.Names})').solution_value > 0.5]
    selected_driver = selected_drivers[0] if len(selected_drivers) > 0 else None

    sln['driver'] = {
        'solution': selected_driver.Names,
        'url': selected_driver.Images if selected_driver is not None else None,
    }
    print(f"\tDriver: {selected_driver.Names}")

    selected_bodies = \
        [body for i, body in bodies.iterrows() if m.get_var_by_name(f'b({body.Names})').solution_value > 0.5]
    selected_body = selected_bodies[0] if len(selected_bodies) > 0 else None
    sln['body'] = {
        'solution': selected_body.Names,
        'url': selected_body.Images if selected_body is not None else None,
    }
    print(f"\tBody: {selected_body.Names}")

    selected_tires = \
        [tire for i, tire in tires.iterrows() if m.get_var_by_name(f't({tire.Names})').solution_value > 0.5]
    selected_tire = selected_tires[0] if len(selected_tires) > 0 else None
    sln['tire'] = {
        'solution': selected_tire.Names,
        'url': selected_tire.Images if selected_tire is not None else None,
    }
    print(f"\tTire: {selected_tire.Names}")

    selected_glider = \
        [glider for i, glider in gliders.iterrows() if m.get_var_by_name(f'g({glider.Names})').solution_value > 0.5]
    selected_glider = selected_glider[0] if len(selected_glider) > 0 else None
    sln['glider'] = {
        'solution': selected_glider.Names,
        'url': selected_glider.Images if selected_glider is not None else None,
    }
    print(f"\tGlider: {selected_glider.Names}")
    print("\n")
    return sln


if __name__ == '__main__':
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(this_file_dir, 'data')

    drivers = load_aggregated(os.path.join(data_dir, 'drivers.csv'))
    bodies = load_aggregated(os.path.join(data_dir, 'bodies.csv'))
    tires = load_aggregated(os.path.join(data_dir, 'tires.csv'))
    gliders = load_aggregated(os.path.join(data_dir, 'gliders.csv'))

    solutions = {}
    stats = lambda x: x.Stats

    with Model(name='best_overall') as model:
        model = setup_model(model, stats, drivers, bodies, tires, gliders)
        if model.solve():
            sln = extract_solution(model, 'Best overall', drivers, bodies, tires, gliders)
            solutions['best_overall'] = sln

    # # group drivers by weight
    # unique_weight = drivers.Size.unique()
    # partitions = {"light": drivers[drivers.Size == "Light"],
    #               "medium": drivers[drivers.Size == "Medium"],
    #               "heavy": drivers[drivers.Size == "Heavy"]}
    #
    # for partition, filtered_drivers in partitions.items():
    #     model = Model(name=f'best_by_weight_{partition}')
    #     model = setup_model(model, stats, filtered_drivers, bodies, tires, gliders)
    #     if model.solve():
    #         sln = extract_solution(model, f'Best for weight {partition}', filtered_drivers, bodies, tires, gliders)
    #         solutions[f'best_by_weight_{partition}'] = sln
    #         model.solution.export(f'best_by_weight_{partition}.json')

    params = {
        'fastest': lambda x: x.Speed,
        'highest_acceleration': lambda x: x.Acceleration,
        'highest_handling': lambda x: x.Handling,
        'highest_invincibility': lambda x: x.Invincibility,
    }

    for name, func in params.items():
        model = Model(name=name)
        model = setup_model(model, func, drivers, bodies, tires, gliders)
        if model.solve():
            sln = extract_solution(model, name, drivers, bodies, tires, gliders)
            solutions[name] = sln

    with open('outputs/solutions.json', 'w') as f:
        f.write(json.dumps(solutions))

    pareto_optimals = {}

    pareto_optimals["speed_acceleration"] = plot_pareto_optimal(drivers, 'Speed', 'Acceleration')
    pareto_optimals["speed_handling"] = plot_pareto_optimal(drivers, 'Speed', 'Handling')
    pareto_optimals["acceleration_handling"] = plot_pareto_optimal(drivers, 'Acceleration', 'Handling')

    with open('outputs/pareto_optimals.json', 'w') as f:
        f.write(json.dumps(pareto_optimals))
