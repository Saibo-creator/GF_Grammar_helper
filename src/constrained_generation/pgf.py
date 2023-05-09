import json
import os
import shlex
import socket
import subprocess
import sys
from typing import List, Union

import requests

DEFAULT_PGF_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "pgf")


class Pgf:

    def __init__(self, pgf: str = "test.pgf"):
        self.pgf = pgf

    def complete(self, sentence: str):
        raise NotImplementedError


class HttpPgf(Pgf):
    DOMAIN: str = "http://localhost"

    def __init__(self,  root_dir=None, pgf: str = "test.pgf", port: int = 41296):
        super().__init__(pgf)
        if root_dir is None:
            root_dir = DEFAULT_PGF_DIR
        self.pgf_dir = root_dir
        self.set_grammar(pgf)

        self.prepare_launch(port=port)
        self._launch_server(root_dir=root_dir, verbose=True)

    def prepare_launch(self, port: int = 41296):
        # Find a free port
        while not is_port_available(port):
            port += 1
        self.port = port
        self.url = HttpPgf.DOMAIN + ":" + str(self.port) + f"/{self.pgf}"

    def _launch_server(self, root_dir: str, verbose: bool = True):
        cmd = f"gf --document-root={root_dir} --server={self.port}"
        if verbose:
            print("Launching server with command: " + cmd)
        # Start the subprocess and detach it from the parent process
        # Split the command string into a list of arguments
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)

        # Wait for the server to be ready
        print(f"visit {self.url} to check if the server is ready")

    def set_grammar(self, pgf: str):
        # check if the grammar is available
        if not self._is_grammar_available(pgf):
            raise Exception(f"Error: the grammar {pgf} is not available in {self.pgf_dir}")

    def complete(self, input: Union[str, List[int]]) -> List[str]:
        processed_input: str = self._preprocess_input_ids(input)
        params = {"command": "complete", 'input_ids': processed_input}

        # Send an HTTP GET request with values
        # pdb.set_trace()
        response = requests.get(self.url, params=params)

        # Parse the response, handle errors
        if response.status_code != 200:
            raise Exception("Error: the server returned status code " + str(response.status_code))

        parsed_response = json.loads(response.text)

        assert len(parsed_response) == 1

        completions = parsed_response[0]['completions']

        return completions

    def get_prefix_allowed_tokens(self, input_ids: str) -> List[int]:
        completions:List[str] = self.complete(input_ids)
        allowed_tokens = [int(x) for x in completions]
        return allowed_tokens

    def _preprocess_input_ids(self, input: Union[str, List[int]]) -> str:
        if type(input) == list:
            input = " ".join([str(x) for x in input])
        if input == "":
            return input
        else:
           return input if input[-1] == " " else input + " "

    def _is_grammar_available(self, pgf):
        path = os.path.join(self.pgf_dir, pgf)
        return os.path.exists(path)


def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False