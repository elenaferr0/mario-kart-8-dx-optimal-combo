from docplex.mp.model import Model
import csv


def build_dict(csv_file_path):
    data_dict = {}
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Read the header row (optional)
            if header:
                for row in reader:
                    if row:  # Ensure the row is not empty
                        key = row[0].strip()
                        values = tuple(row[1:])
                        data_dict[key] = list(map(int, values))
            else:
                print(f"Warning: CSV file at '{csv_file_path}' is empty.")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'.")
    return data_dict


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
    driver_score = m.sum(d[i] * sum(drivers[i]) for i in drivers.keys())
    body_score = m.sum(b[i] * sum(bodies[i]) for i in bodies.keys())
    tire_score = m.sum(t[i] * sum(tires[i]) for i in tires.keys())
    glider_score = m.sum(g[i] * sum(gliders[i]) for i in gliders.keys())
    m.maximize(driver_score + body_score + tire_score + glider_score)

    return m


def print_sln(m: Model) -> None:
    obj = m.objective_value
    print("Model solved with objective: {:g}".format(obj))

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
    drivers = build_dict('data/drivers.csv')
    bodies = build_dict('data/bodies.csv')
    tires = build_dict('data/tires.csv')
    gliders = build_dict('data/gliders.csv')

    with Model(name='mk-8-dx-stats') as model:
        model = get_best_combo(model)
        if model.solve():
            print_sln(model)
            model.solution.export('solution.json')
