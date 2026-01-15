import pandas as pd

from road_traffic.parser import extract_records, payload_to_dataframe


def test_extract_records_flat_payload():
    payload = {
        "current_page": 1,
        "data": [
            {"id": 1, "year": 2000, "road_name": "A1"},
            {"id": 2, "year": 2001, "road_name": "A2"},
        ],
    }

    records = extract_records(payload)

    assert isinstance(records, list)
    assert records[0]["id"] == 1
    assert records[0]["road_name"] == "A1"
    assert records[1]["year"] == 2001


def test_extract_records_jsonapi_payload():
    payload = {
        "data": [
            {"id": "abc", "attributes": {"year": 2020, "value": 10}},
            {"id": "def", "attributes": {"year": 2021, "value": 12}},
        ]
    }

    records = extract_records(payload)

    assert records[0]["id"] == "abc"
    assert records[0]["year"] == 2020
    assert records[1]["value"] == 12


def test_payload_to_dataframe_returns_dataframe():
    payload = {"data": [{"id": 1, "year": "2000"}, {"id": 2, "year": "2001"}]}
    df = payload_to_dataframe(payload)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "year"]
    assert df["year"].dtype.kind in ("i", "f")
