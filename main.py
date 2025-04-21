import os, io
from typing import Dict

from docplex.mp.model import Model

from models.base_stats import BaseStats
from models.driver_stats import Driver
from models.body_stats import Body
from models.glider_stats import Glider
from models.tire_stats import Tire
from models.parser import parse_csv_data


def best_overall(m: Model, drivers: Dict[str, Driver], bodies: Dict[str, Body], tires: Dict[str, Tire],
                 gliders: Dict[str, Glider]) -> Model:
    # Create decision variables
    d = {i: m.binary_var(name=f'd({i})') for i in drivers.keys()}
    b = {i: m.binary_var(name=f'b({i})') for i in bodies.keys()}
    t = {i: m.binary_var(name=f't({i})') for i in tires.keys()}
    g = {i: m.binary_var(name=f'g({i})') for i in gliders.keys()}

    # Constraints (there can be at most one1 of each type)
    m.add_constraint(m.sum(d[i] for i in drivers.keys()) <= 1, 'one_driver')
    m.add_constraint(m.sum(b[i] for i in bodies.keys()) <= 1, 'one_body')
    m.add_constraint(m.sum(t[i] for i in tires.keys()) <= 1, 'one_tire')
    m.add_constraint(m.sum(g[i] for i in gliders.keys()) <= 1, 'one_glider')

    # Maximize the total score
    driver_score = m.sum(d[i] * drivers[i].sum() for i in drivers.keys())
    body_score = m.sum(b[i] * bodies[i].sum() for i in bodies.keys())
    tire_score = m.sum(t[i] * tires[i].sum() for i in tires.keys())
    glider_score = m.sum(g[i] * gliders[i].sum() for i in gliders.keys())

    m.maximize(driver_score + body_score + tire_score + glider_score)
    return m


def best_by_param(m: Model,
                  param_extractor,
                  drivers: Dict[str, Driver], bodies: Dict[str, Body], tires: Dict[str, Tire],
                  gliders: Dict[str, Glider]) -> Model:
    # Create decision variables
    d = {i: m.binary_var(name=f'd({i})') for i in drivers.keys()}
    b = {i: m.binary_var(name=f'b({i})') for i in bodies.keys()}
    t = {i: m.binary_var(name=f't({i})') for i in tires.keys()}
    g = {i: m.binary_var(name=f'g({i})') for i in gliders.keys()}

    # Constraints (there can be at most one1 of each type)
    m.add_constraint(m.sum(d[i] for i in drivers.keys()) <= 1, 'one_driver')
    m.add_constraint(m.sum(b[i] for i in bodies.keys()) <= 1, 'one_body')
    m.add_constraint(m.sum(t[i] for i in tires.keys()) <= 1, 'one_tire')
    m.add_constraint(m.sum(g[i] for i in gliders.keys()) <= 1, 'one_glider')

    # Maximize the total score
    driver_score = m.sum(d[i] * param_extractor(drivers[i]) for i in drivers.keys())
    body_score = m.sum(b[i] * param_extractor(bodies[i]) for i in bodies.keys())
    tire_score = m.sum(t[i] * param_extractor(tires[i]) for i in tires.keys())
    glider_score = m.sum(g[i] * param_extractor(gliders[i]) for i in gliders.keys())

    m.maximize(driver_score + body_score + tire_score + glider_score)

    return m


def extract_solution(m: Model, problem: str, drivers: Dict[str, Driver], bodies: Dict[str, Body] = None,
                     tires: Dict[str, Tire] = None, gliders: Dict[str, Glider] = None) -> Dict[str, BaseStats]:
    sln = {}
    obj = m.objective_value
    print(f"{problem}, Objective value: {obj}")

    print("Optimal solution:")
    selected_driver = [i for i in drivers.keys() if m.get_var_by_name(f'd({i})').solution_value > 0.5]
    sln['driver'] = {
        'solution': selected_driver[0] if selected_driver else None,
        'url': drivers[selected_driver[0]].image_url if selected_driver else None,
    }
    print(f"\tDriver: {selected_driver[0]}" if selected_driver else "No driver selected")

    selected_body = [i for i in bodies.keys() if m.get_var_by_name(f'b({i})').solution_value > 0.5]
    sln['body'] = {
        'solution': selected_body[0] if selected_body else None,
        'url': bodies[selected_body[0]].image_url if selected_body else None,
    }
    print(f"\tBody: {selected_body[0]}" if selected_body else "No body selected")

    selected_tire = [i for i in tires.keys() if m.get_var_by_name(f't({i})').solution_value > 0.5]
    sln['tire'] = {
        'solution': selected_tire[0] if selected_tire else None,
        'url': tires[selected_tire[0]].image_url if selected_tire else None,
    }
    print(f"\tTire: {selected_tire[0]}" if selected_tire else "No tire selected")

    selected_glider = [i for i in gliders.keys() if m.get_var_by_name(f'g({i})').solution_value > 0.5]
    sln['glider'] = {
        'solution': selected_glider[0] if selected_glider else None,
        'url': gliders[selected_glider[0]].image_url if selected_glider else None,
    }
    print(f"\tGlider: {selected_glider[0]}" if selected_glider else "No glider selected")
    print("\n")
    return sln

if __name__ == '__main__':
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(this_file_dir, 'data')

    drivers: Dict[str, Driver] = parse_csv_data(data_dir + '/drivers.csv', Driver)
    bodies: Dict[str, Body] = parse_csv_data(data_dir + '/bodies.csv', Body)
    tires: Dict[str, Tire] = parse_csv_data(data_dir + '/tires.csv', Tire)
    gliders: Dict[str, Glider] = parse_csv_data(data_dir + '/gliders.csv', Glider)

    solutions = {}

    with Model(name='best_overall') as model:
        model = best_overall(model, drivers, bodies, tires, gliders)
        if model.solve():
            sln = extract_solution(model, 'Best overall', drivers, bodies, tires, gliders)
            solutions['best_overall'] = sln
            model.solution.export('best_overall.json')

    # group drivers by weight
    light = {d: drivers[d] for d in drivers if drivers[d].size == 'Light'}
    medium = {d: drivers[d] for d in drivers if drivers[d].size == 'Medium'}
    heavy = {d: drivers[d] for d in drivers if drivers[d].size == 'Heavy'}

    partitions = {"light": light, "medium": medium, "heavy": heavy}

    for partition, filtered_drivers in partitions.items():
        model = Model(name=f'best_by_weight_{partition}')
        model = best_overall(model, filtered_drivers, bodies, tires, gliders)
        if model.solve():
            sln = extract_solution(model, f'Best for weight {partition}', filtered_drivers, bodies, tires, gliders)
            solutions[f'best_by_weight_{partition}'] = sln
            model.solution.export(f'best_by_weight_{partition}.json')

    params = {
        'fastest': lambda x: x.speed,
        'highest_acceleration': lambda x: x.acceleration,
        'highest_handling': lambda x: x.handling,
        'highest_invincibility': lambda x: x.invincibility,
    }

    for name, func in params.items():
        model = Model(name=name)
        model = best_by_param(model, func, drivers, bodies, tires, gliders)
        if model.solve():
            sln = extract_solution(model, name, drivers, bodies, tires, gliders)
            solutions[name] = sln
            model.solution.export(f"best_by_param_{name}.json")

    print("Solutions:", solutions)
