from road_traffic.pipeline import fetch_aadf_sample, run


def test_fetch_aadf_sample_returns_rows(monkeypatch):
    class DummyClient:
        def get_json(self, path, params=None):
            return {
                "data": [
                    {"id": 1, "year": 2020, "all_motor_vehicles": 100},
                    {"id": 2, "year": 2021, "all_motor_vehicles": 150},
                ]
            }

    monkeypatch.setattr("road_traffic.pipeline.RoadTrafficClient", lambda: DummyClient())

    df = fetch_aadf_sample(page_size=2)

    assert len(df) == 2
    assert "year" in df.columns
    assert "all_motor_vehicles" in df.columns


def test_run_writes_csv_and_png(tmp_path, monkeypatch):
    class DummyClient:
        def get_json(self, path, params=None):
            return {
                "data": [
                    {"id": 1, "year": 2020, "all_motor_vehicles": 100},
                    {"id": 2, "year": 2020, "all_motor_vehicles": 120},
                    {"id": 3, "year": 2021, "all_motor_vehicles": 150},
                ]
            }

    monkeypatch.setattr("road_traffic.pipeline.RoadTrafficClient", lambda: DummyClient())

    csv_path, png_path = run(output_dir=str(tmp_path), page_size=3)

    assert csv_path.exists()
    assert png_path.exists()
