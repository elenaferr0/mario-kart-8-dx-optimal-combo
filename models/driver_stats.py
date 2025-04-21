from models.base_stats import BaseStats


class Driver(BaseStats):
    def __init__(self, name, image_url, size, speed_ground, speed_water, speed_air,
                 speed_anti_gravity, acceleration, weight, handling_ground,
                 handling_water, handling_air, handling_anti_gravity,
                 off_road_traction, mini_turbo, invincibility, on_road_traction):
        super().__init__(speed_ground, speed_water, speed_air, speed_anti_gravity,
                         acceleration, weight, handling_ground, handling_water,
                         handling_air, handling_anti_gravity, off_road_traction,
                         mini_turbo, invincibility, on_road_traction)
        self.name = name
        self.image_url = image_url
        self.size = size

    def __repr__(self):
        return (f"Driver(name='{self.name}'\nimage_url='{self.image_url}'\nsize='{self.size}'\n"
                f"{super().__repr__()})")
