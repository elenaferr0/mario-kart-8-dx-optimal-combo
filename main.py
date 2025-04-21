import os
from typing import Dict

from docplex.mp.model import Model

from models.driver_stats import Driver
from models.body_stats import Body
from models.glider_stats import Glider
from models.tire_stats import Tire
from models.parser import parse_csv_data


def get_best_combo(m: Model) -> Model:
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


def print_sln(m: Model) -> None:
    obj = m.objective_value
    print("Objective fun: {:g}".format(obj))

    print("Optimal solution:")
    selected_driver = [i for i in drivers.keys() if m.get_var_by_name(f'd({i})').solution_value > 0.5]
    print(f"\tDriver: {selected_driver[0]}" if selected_driver else "No driver selected")

    selected_body = [i for i in bodies.keys() if m.get_var_by_name(f'b({i})').solution_value > 0.5]
    print(f"\tBody: {selected_body[0]}" if selected_body else "No body selected")

    selected_tire = [i for i in tires.keys() if m.get_var_by_name(f't({i})').solution_value > 0.5]
    print(f"\tTire: {selected_tire[0]}" if selected_tire else "No tire selected")

    selected_glider = [i for i in gliders.keys() if m.get_var_by_name(f'g({i})').solution_value > 0.5]
    print(f"\tGlider: {selected_glider[0]}" if selected_glider else "No glider selected")


if __name__ == '__main__':
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(this_file_dir, 'data')

    drivers: Dict[str, Driver] = parse_csv_data(data_dir + '/drivers.csv', Driver)
    bodies: Dict[str, Body] = parse_csv_data(data_dir + '/bodies.csv', Body)
    tires: Dict[str, Tire] = parse_csv_data(data_dir + '/tires.csv', Tire)
    gliders: Dict[str, Glider] = parse_csv_data(data_dir + '/gliders.csv', Glider)

    with Model(name='mk-8-dx-stats') as model:
        model = get_best_combo(model)
        if model.solve():
            print_sln(model)
            model.solution.export('solution.json')
