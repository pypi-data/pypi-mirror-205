import logging
from typing import Any, Optional

from phable.http import request
from phable.scram import get_auth_token
from phable.kinds import Grid
from phable.json_parser import json_to_grid  # parse_kinds

logger = logging.getLogger(__name__)

# TODO:  Supports arbitrary GET and POST calls
# https://project-haystack.org/forum/topic/930

# TODO:  Refactor to reduce code duplication


class Phable:
    """
    A client interface to a Haystack Server used for authentication and Haystack ops.
    """

    def __init__(
        self, uri: str, username: str, password: str, format: str = "application/json"
    ):
        self._uri = uri
        self._username = username
        self._password = password
        self._format = format

    def __enter__(self):
        self._auth_token = get_auth_token(
            self._uri + "/about", self._username, self._password
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def about(self):
        """
        Executes the Haystack about op, which queries basic information about
        the server.
        """
        headers = {
            "Authorization": f"BEARER authToken={self._auth_token}",
            "Accept": self._format,
        }

        url = f"{self._uri}/about"

        response = request(url, headers=headers)

        return response.json()

    def close(self) -> None:
        """
        Executes the Haystack close op, which closes the current
        authentication session.
        """
        headers = {"Authorization": f"BEARER authToken={self._auth_token}"}
        url = f"{self._uri}/close"

        response = request(url, headers)

        # TODO:  Check the response and verify its cool!

        return None

    def read(self, grid: Grid) -> Grid:
        """
        https://project-haystack.org/doc/docHaystack/Ops/#read
        """
        url = f"{self._uri}/read"

        headers = {
            "Authorization": f"BEARER authToken={self._auth_token}",
            "Accept": self._format,
        }
        response = request(url=url, data=grid.to_json(), headers=headers, method="POST")

        return json_to_grid(response.json())

    def eval(self, grid: Grid) -> Grid:
        url = f"{self._uri}/eval"

        headers = {
            "Authorization": f"BEARER authToken={self._auth_token}",
            "Accept": self._format,
        }
        response = request(url=url, data=grid.to_json(), headers=headers, method="POST")

        return json_to_grid(response.json())

    def his_read(self, grid: Grid) -> Grid:
        url = f"{self._uri}/hisRead"

        headers = {
            "Authorization": f"BEARER authToken={self._auth_token}",
            "Accept": self._format,
        }
        response = request(url=url, data=grid.to_json(), headers=headers, method="POST")

        return json_to_grid(response.json())

    def his_write(self, grid: Grid) -> Grid:
        url = f"{self._uri}/hisWrite"

        headers = {
            "Authorization": f"BEARER authToken={self._auth_token}",
            "Accept": self._format,
        }
        response = request(url=url, data=grid.to_json(), headers=headers, method="POST")

        return json_to_grid(response.json())
