from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from road_traffic.api_client import RoadTrafficClient
from road_traffic.parser import payload_to_dataframe


def fetch_aadf_sample(page_size=100):
    client = RoadTrafficClient()
    payload = client.get_json("/api/average-annual-daily-flow", params={"page[size]": page_size})
    return payload_to_dataframe(payload)


def run(output_dir="outputs", page_size=100):
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = fetch_aadf_sample(page_size=page_size)

    csv_path = out_dir / "API-Road-trafficsample.csv"
    df.to_csv(csv_path, index=False)

    png_path = out_dir / "Road-traffic_trend.png"

    if "year" in df.columns and "all_motor_vehicles" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce")
        values = pd.to_numeric(df["all_motor_vehicles"], errors="coerce")

        tmp = pd.DataFrame({"year": years, "all_motor_vehicles": values}).dropna()
        trend = tmp.groupby("year")["all_motor_vehicles"].mean()

        if len(trend) >= 2:
            plt.figure()
            trend.plot()
            plt.title("sample data: mean of all vehicles by year")
            plt.xlabel("Year")
            plt.ylabel("Mean of all vehicles")
            plt.tight_layout()
            plt.savefig(png_path)
            plt.close()

    return csv_path, png_path


if __name__ == "__main__":
    run()
