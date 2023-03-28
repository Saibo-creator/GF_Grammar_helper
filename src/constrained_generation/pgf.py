import json
from typing import List

import requests


class Pgf:

    def __init__(self, pgf: str = "test.pgf"):
        self.pgf = pgf

    def complete(self, sentence: str):
        raise NotImplementedError


class ServerPgf(Pgf):

    def __init__(self, pgf: str = "test.pgf", url="https://localhost", port=41296):
        super().__init__(pgf)
        self.url = url + ":" + str(port) + f"/{pgf}"

    def complete(self, input: str) -> List[str]:
        params = {"command": "complete", 'input': input}

        # Send an HTTP GET request with values
        response = requests.get(self.url, params=params)

        parsed_response = json.loads(response.text)

        assert len(parsed_response) == 1

        completions = parsed_response[0]['completions']

        return completions
