from models.base_stats import BaseStats


class Body(BaseStats):
    def __init__(self, name, image_url, vehicle_type, speed_ground, speed_water, speed_air,
                 speed_anti_gravity, acceleration, weight, handling_ground,
                 handling_water, handling_air, handling_anti_gravity,
                 off_road_traction, mini_turbo, invincibility, on_road_traction):
        super().__init__(speed_ground, speed_water, speed_air, speed_anti_gravity,
                         acceleration, weight, handling_ground, handling_water,
                         handling_air, handling_anti_gravity, off_road_traction,
                         mini_turbo, invincibility, on_road_traction)
        self.name = name
        self.image_url = image_url
        self.vehicle_type = vehicle_type

    def __repr__(self):
        return (f"Body(name='{self.name}', image_url='{self.image_url}', vehicle_type='{self.vehicle_type}', "
                f"{super().__repr__()})")
