from models.base_stats import BaseStats


class Glider(BaseStats):
    def __init__(self, name, image_url, speed_ground, speed_water, speed_air,
                 speed_anti_gravity, acceleration, weight, handling_ground,
                 handling_water, handling_air, handling_anti_gravity,
                 off_road_traction, mini_turbo, invincibility, on_road_traction):
        super().__init__(speed_ground, speed_water, speed_air, speed_anti_gravity,
                         acceleration, weight, handling_ground, handling_water,
                         handling_air, handling_anti_gravity, off_road_traction,
                         mini_turbo, invincibility, on_road_traction)
        self.name = name
        self.image_url = image_url

    def __repr__(self):
        return f"Glider(name='{self.name}', image_url='{self.image_url}', {super().__repr__()})"
