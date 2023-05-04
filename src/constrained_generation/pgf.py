import json
import shlex
import socket
import subprocess
from typing import List, Union

import requests


class Pgf:

    def __init__(self, pgf: str = "test.pgf"):
        self.pgf = pgf

    def complete(self, sentence: str):
        raise NotImplementedError


class HttpPgf(Pgf):
    DOMAIN: str = "http://localhost"

    def __init__(self,  root_dir: str = ".", pgf: str = "test.pgf", port: int = 41296):
        super().__init__(pgf)
        self.set_grammar(pgf)

        # Find a free port
        while not is_port_available(port):
            port += 1
        self.port = port
        self._launch_server(root_dir=root_dir, verbose=True)

    def _launch_server(self, root_dir: str, verbose: bool = True):
        cmd = f"gf --document-root={root_dir} --server={self.port}"
        if verbose:
            print("Launching server with command: " + cmd)
        # Start the subprocess and detach it from the parent process
        # Split the command string into a list of arguments
        args = shlex.split(cmd)
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)

    def set_grammar(self, pgf: str):
        self.pgf = pgf
        self.url = HttpPgf.DOMAIN + ":" + str(self.port) + f"/{pgf}"

    def complete(self, input: Union[str, List[int]]) -> List[str]:
        processed_input: str = self._preprocess_input_ids(input)
        params = {"command": "complete", 'input_ids': processed_input}

        # Send an HTTP GET request with values
        # pdb.set_trace()
        response = requests.get(self.url, params=params)

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


def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False