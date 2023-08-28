from typing import List
from unittest import TestCase

from src.constrained_generation.gf_runtime import GFServerRuntime


class TestGFServerRuntime(TestCase):
    def setUp(self) -> None:
        super().setUp()
        pgf = "FoodRepeat.pgf"
        pgf_dir = "/Users/saibo/Research/Projects/GCD/GF-Grammar-Factory/asset/GF-grammars/pgf"
        self.gf_server = GFServerRuntime(default_pgf=pgf, grammar_dir=pgf_dir)

    def tearDown(self) -> None:

        super().tearDown()
        self.gf_server.clear()

    def test_complete(self):
        first_completions: List[str] = self.gf_server.complete(input_tokens=[])
        second_completions: List[str] = self.gf_server.complete(input_tokens=["this"])

        self.assertEqual(first_completions, ["that", "this"])
        self.assertEqual(
            second_completions,
            [
                "Italian",
                "boring",
                "cheese",
                "delicious",
                "expensive",
                "fish",
                "fresh",
                "very",
                "warm",
                "wine",
            ],
        )
