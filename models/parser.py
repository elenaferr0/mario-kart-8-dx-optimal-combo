import csv
from typing import Dict

from models.base_stats import BaseStats
from models.body_stats import Body
from models.driver_stats import Driver
from models.glider_stats import Glider
from models.tire_stats import Tire


def parse_csv_data(csv_file_path, target_class) -> Dict[str, BaseStats]:
    # Check for valid model type
    if target_class not in (Body, Driver, Tire, Glider):
        raise Exception(
            f"Error: Invalid model type '{target_class}'.  Must be one of 'body', 'driver', 'tire', or 'glider'.")

    data_objects = {}
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)  # Read the header row (optional)
        if header:
            for row in reader:
                # Convert numerical values to integers, handle empty strings
                row_data = {
                    header[i]: int(value) if value.isdigit() else value
                    for i, value in enumerate(row)
                }
                try:
                    # Unpack the row data, handling potential missing keys
                    if target_class == Body:
                        obj = target_class(
                            name=row_data['Name'],
                            image_url=row_data['Image URL'],
                            vehicle_type=row_data['Vehicle Type'],
                            speed_ground=row_data['Speed (Ground)'], speed_water=row_data['Speed (Water)'],
                            speed_air=row_data['Speed (Air)'],
                            speed_anti_gravity=row_data['Speed (Anti-Gravity)'],
                            acceleration=row_data['Acceleration (AC)'], weight=row_data['Weight (WG)'],
                            handling_ground=row_data['Handling (Ground)'],
                            handling_water=row_data['Handling (Water)'],
                            handling_air=row_data['Handling (Air)'],
                            handling_anti_gravity=row_data['Handling (Anti-Gravity)'],
                            off_road_traction=row_data['(Off-Road) Traction (OF)'],
                            mini_turbo=row_data['Mini-Turbo (MT)'],
                            invincibility=row_data['Invincibility (IV)'],
                            on_road_traction=row_data['On-Road Traction (ON)']
                        )
                    elif target_class == Driver:
                        obj = target_class(
                            name=row_data['Name'],
                            image_url=row_data['Image URL'],
                            size=row_data['Size'],
                            speed_ground=row_data['Speed (Ground)'],
                            speed_water=row_data['Speed (Water)'],
                            speed_air=row_data['Speed (Air)'],
                            speed_anti_gravity=row_data['Speed (Anti-Gravity)'],
                            acceleration=row_data['Acceleration (AC)'],
                            weight=row_data['Weight (WG)'],
                            handling_ground=row_data['Handling (Ground)'],
                            handling_water=row_data['Handling (Water)'],
                            handling_air=row_data['Handling (Air)'],
                            handling_anti_gravity=row_data['Handling (Anti-Gravity)'],
                            off_road_traction=row_data['(Off-Road) Traction (OF)'],
                            mini_turbo=row_data['Mini-Turbo (MT)'],
                            invincibility=row_data['Invincibility (IV)'],
                            on_road_traction=row_data['On-Road Traction (ON)']
                        )
                    elif target_class == Tire:
                        obj = target_class(
                            name=row_data['Name'],
                            image_url=row_data['Image URL'],
                            speed_ground=row_data['Speed (Ground)'],
                            speed_water=row_data['Speed (Water)'],
                            speed_air=row_data['Speed (Air)'],
                            speed_anti_gravity=row_data['Speed (Anti-Gravity)'],
                            acceleration=row_data['Acceleration (AC)'],
                            weight=row_data['Weight (WG)'],
                            handling_ground=row_data['Handling (Ground)'],
                            handling_water=row_data['Handling (Water)'],
                            handling_air=row_data['Handling (Air)'],
                            handling_anti_gravity=row_data['Handling (Anti-Gravity)'],
                            off_road_traction=row_data['(Off-Road) Traction (OF)'],
                            mini_turbo=row_data['Mini-Turbo (MT)'],
                            invincibility=row_data['Invincibility (IV)'],
                            on_road_traction=row_data['On-Road Traction (ON)']
                        )
                    else:  # Glider
                        obj = target_class(
                            name=row_data['Name'],
                            image_url=row_data['Image URL'],
                            speed_ground=row_data['Speed (Ground)'],
                            speed_water=row_data['Speed (Water)'],
                            speed_air=row_data['Speed (Air)'],
                            speed_anti_gravity=row_data['Speed (Anti-Gravity)'],
                            acceleration=row_data['Acceleration (AC)'],
                            weight=row_data['Weight (WG)'],
                            handling_ground=row_data['Handling (Ground)'],
                            handling_water=row_data['Handling (Water)'],
                            handling_air=row_data['Handling (Air)'],
                            handling_anti_gravity=row_data['Handling (Anti-Gravity)'],
                            off_road_traction=row_data['(Off-Road) Traction (OF)'],
                            mini_turbo=row_data['Mini-Turbo (MT)'],
                            invincibility=row_data['Invincibility (IV)'],
                            on_road_traction=row_data['On-Road Traction (ON)']
                        )
                    data_objects[row_data['Name']] = obj
                except KeyError as e:
                    print(f"Error: Missing key(s) in row: {e}.  Skipping row.")
                    continue  # Skip to the next row

    return data_objects
