from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests

class RoadTrafficApiError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code

@dataclass
class RoadTrafficClient:
    base_url: str = "https://roadtraffic.dft.gov.uk"
    timeout_seconds: int = 20

    def build_url(self, path: str) -> str:
        if path.startswith("/"):
            return self.base_url.rstrip("/") + path
        return self.base_url.rstrip("/") + "/" + path

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self.build_url(path)

        try:
            response = requests.get(
                url,
                params=params,
                headers={"Accept": "application/json"},
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise RoadTrafficApiError(f"request error calling the API: {exc}") from exc

        if response.status_code >= 400:
            raise RoadTrafficApiError(
                f"API error {response.status_code} for {url}",
                status_code=response.status_code,
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise RoadTrafficApiError("API response was invalid JSON", status_code=response.status_code) from exc

        if not isinstance(payload, dict):
            raise RoadTrafficApiError("not a JSON object at the top level", status_code=response.status_code)

        return payload
