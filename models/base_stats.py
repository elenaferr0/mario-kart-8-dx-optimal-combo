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
        return (f"BaseStats(speed_ground={self.speed_ground}, speed_water={self.speed_water}, "
                f"speed_air={self.speed_air}, speed_anti_gravity={self.speed_anti_gravity}, "
                f"acceleration={self.acceleration}, weight={self.weight}, "
                f"handling_ground={self.handling_ground}, handling_water={self.handling_water}, "
                f"handling_air={self.handling_air}, handling_anti_gravity={self.handling_anti_gravity}, "
                f"off_road_traction={self.off_road_traction}, mini_turbo={self.mini_turbo}, "
                f"invincibility={self.invincibility}, on_road_traction={self.on_road_traction})")

    def sum(self):
        return (
            self.speed_ground + self.speed_water + self.speed_air + self.speed_anti_gravity +
            self.acceleration + self.weight + self.handling_ground + self.handling_water +
            self.handling_air + self.handling_anti_gravity + self.off_road_traction +
            self.mini_turbo + self.invincibility + self.on_road_traction
        )