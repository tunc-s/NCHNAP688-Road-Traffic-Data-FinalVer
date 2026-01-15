import pandas as pd

def extract_records(payload):
    data = payload.get("data", [])

    if not isinstance(data, list):
        raise ValueError("Expected 'data' to be a list")

    if len(data) == 0:
        return []

    first = data[0]

    if isinstance(first, dict) and "attributes" in first and isinstance(first.get("attributes"), dict):
        rows = []
        for item in data:
            row = dict(item.get("attributes", {}))
            if "id" in item:
                row["id"] = item["id"]
            rows.append(row)
        return rows

    return data


def payload_to_dataframe(payload):
    records = extract_records(payload)
    df = pd.DataFrame(records)

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df
