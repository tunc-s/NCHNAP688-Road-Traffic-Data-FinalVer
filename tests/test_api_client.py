import requests

from road_traffic.api_client import RoadTrafficApiError, RoadTrafficClient


def test_build_url_adds_slash():
    client = RoadTrafficClient(base_url="https://example.com")
    assert client.build_url("api/test") == "https://example.com/api/test"


def test_build_url_keeps_existing_slash():
    client = RoadTrafficClient(base_url="https://example.com")
    assert client.build_url("/api/test") == "https://example.com/api/test"


def test_get_json_returns_dict(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"data": [1, 2, 3]}

    def fake_get(url, params=None, headers=None, timeout=None):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    client = RoadTrafficClient(base_url="https://example.com")
    result = client.get_json("/api/test", params={"page[size]": 5})
    assert result["data"] == [1, 2, 3]


def test_get_json_raises_on_http_error(monkeypatch):
    class DummyResponse:
        status_code = 404

        def json(self):
            return {"error": "not found"}

    def fake_get(url, params=None, headers=None, timeout=None):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    client = RoadTrafficClient(base_url="https://example.com")

    try:
        client.get_json("/api/missing")
        assert False
    except RoadTrafficApiError as exc:
        assert exc.status_code == 404


def test_get_json_raises_on_request_exception(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        raise requests.RequestException("Connection failed")

    monkeypatch.setattr(requests, "get", fake_get)

    client = RoadTrafficClient(base_url="https://example.com")

    try:
        client.get_json("/api/test")
        assert False
    except RoadTrafficApiError as exc:
        assert "error" in str(exc)
