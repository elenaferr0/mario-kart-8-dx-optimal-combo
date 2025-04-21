class BaseStats:
    def __init__(self, speed_ground, speed_water, speed_air, speed_anti_gravity,
                 acceleration, weight, handling_ground, handling_water,
                 handling_air, handling_anti_gravity, off_road_traction,
                 mini_turbo, invincibility, on_road_traction):
        self.speed_ground = speed_ground
        self.speed_water = speed_water
        self.speed_air = speed_air
        self.speed_anti_gravity = speed_anti_gravity
        self.acceleration = acceleration
        self.weight = weight
        self.handling_ground = handling_ground
        self.handling_water = handling_water
        self.handling_air = handling_air
        self.handling_anti_gravity = handling_anti_gravity
        self.off_road_traction = off_road_traction
        self.mini_turbo = mini_turbo
        self.invincibility = invincibility
        self.on_road_traction = on_road_traction

    def __repr__(self):
        return (f"BaseStats(speed_ground={self.speed_ground}\n speed_water={self.speed_water}\n "
                f"speed_air={self.speed_air}\n speed_anti_gravity={self.speed_anti_gravity}\n "
                f"acceleration={self.acceleration}\n weight={self.weight}\n "
                f"handling_ground={self.handling_ground}\n handling_water={self.handling_water}\n "
                f"handling_air={self.handling_air}\n handling_anti_gravity={self.handling_anti_gravity}\n "
                f"off_road_traction={self.off_road_traction}\n mini_turbo={self.mini_turbo}\n "
                f"invincibility={self.invincibility}\n on_road_traction={self.on_road_traction})")

    def sum(self):
        return (
            self.speed_ground + self.speed_water + self.speed_air + self.speed_anti_gravity +
            self.acceleration + self.weight + self.handling_ground + self.handling_water +
            self.handling_air + self.handling_anti_gravity + self.off_road_traction +
            self.mini_turbo + self.invincibility + self.on_road_traction
        )

    @property
    def speed(self):
        return (
            self.speed_ground + self.speed_water + self.speed_air + self.speed_anti_gravity
        )

    @property
    def handling(self):
        return (
            self.handling_ground + self.handling_water + self.handling_air + self.handling_anti_gravity
        )