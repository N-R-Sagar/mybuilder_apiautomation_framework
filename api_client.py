import requests
from typing import Optional, Dict, Any


class APIClientError(Exception):
    pass


class APIClient:
    """Small HTTP client wrapper for API tests.

    - Manages authentication token (Bearer)
    - Provides request wrapper with timeout and basic error handling
    - Exposes a method to simulate expired tokens for negative tests
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout
        self.token: Optional[str] = None

    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/Authenticate/Login"
        resp = self.session.post(url, json={"userName": username, "password": password}, timeout=self.timeout)
        if resp.status_code != 200:
            raise APIClientError(f"Authentication failed: {resp.status_code} {resp.text}")
        data = resp.json()
        # Accept token in common fields
        token = data.get("token") or data.get("access_token") or data.get("data")
        if isinstance(token, dict):
            token = token.get("token") or token.get("access_token")
        if not token:
            # fall back to entire response as token (some APIs wrap differently)
            token = data
        self.token = token
        # set Authorization header
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return data

    def set_token(self, token: Optional[str]):
        self.token = token
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.session.headers.pop("Authorization", None)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.Timeout as e:
            raise APIClientError("timeout") from e
        except requests.RequestException as e:
            raise APIClientError("request failed") from e
        return resp

    def request_raise_on_unauthorized(self, method: str, path: str, **kwargs) -> requests.Response:
        """Perform request and raise APIClientError on 401 to exercise auth branches."""
        resp = self.request(method, path, **kwargs)
        if resp.status_code == 401:
            raise APIClientError("unauthorized")
        return resp
