import pandas as pd

speed_headers = ["GroundSpeed", "WaterSpeed", "AirSpeed", "Anti-GravitySpeed"]
handling_headers = ["GroundHandling", "WaterHandling", "AirHandling", "Anti-GravityHandling"]

stats_headers = [*speed_headers, "Acceleration", "Weight", *handling_headers, "Off-RoadTraction", "Mini-Turbo",
                 "Invincibility", "On-RoadTraction"]

def load_aggregated(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    grouped = df.groupby(stats_headers).agg(
        Names=("Name", lambda x: ','.join(x.astype(str))),
        Images=("ImageURL", lambda x: ','.join(x.astype(str))),
    ).reset_index()

    grouped['Speed'] = grouped[speed_headers].sum(axis=1)
    grouped['Handling'] = grouped[handling_headers].sum(axis=1)
    grouped['Stats'] = grouped[stats_headers].sum(axis=1)
    return grouped
