from typing import List
from unittest import TestCase

from src.constrained_generation.gf_runtime import GFServerRuntime
from src.config.config import NEW_PGF_AUTO_GEN_DIR, PGF_ASSET_DIR


class TestGFServerRuntime(TestCase):
    def setUp(self) -> None:
        super().setUp()
        pgf = "FoodRepeat.pgf"
        pgf_dir = PGF_ASSET_DIR
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


class TestGFServerRuntimeIE(TestCase):
    def setUp(self) -> None:
        super().setUp()
        pgf_dir = NEW_PGF_AUTO_GEN_DIR
        task = "IE"
        grammar_type = "fe"
        dataset = "wikinre"
        grammar_name = f"{task}_{grammar_type}_{dataset}_0.pgf"
        relative_path = f"{task}/{grammar_type}/{dataset}/{grammar_name}"
        self.gf_server = GFServerRuntime(default_pgf=relative_path, grammar_dir=pgf_dir)

    def tearDown(self) -> None:
        super().tearDown()
        self.gf_server.clear()

    def test_complete(self):
        completions: List[str] = self.gf_server.complete(input_tokens=[])

        self.assertEqual(completions, ["2", "518"])

        completions: List[str] = self.gf_server.complete(input_tokens=["518"])
        self.assertEqual(completions, ["29879"])

        completions: List[str] = self.gf_server.complete(input_tokens=["518", "29879"])
        self.assertEqual(completions, ["29962"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["518", "29879", "29962"]
        )
        self.assertEqual(len(completions), 3572)

    def test_random_decode(self):
        times = self.gf_server.random_decode(n=512, tokens2exclude={"2"})
        print(times)


class TestGFServerRuntimeED(TestCase):
    def setUp(self) -> None:
        super().setUp()
        pgf_dir = NEW_PGF_AUTO_GEN_DIR
        task = "ED"
        grammar_type = "canonical"
        dataset = "aida"
        grammar_name = f"{task}_{grammar_type}_{dataset}_0.pgf"
        relative_path = f"{task}/{grammar_type}/{dataset}/{grammar_name}"
        self.gf_server = GFServerRuntime(default_pgf=relative_path, grammar_dir=pgf_dir)

    def tearDown(self) -> None:
        super().tearDown()
        self.gf_server.clear()

    def test_complete(self):
        completions: List[str] = self.gf_server.complete(input_tokens=[])

        self.assertEqual(completions, ["5546"])

        completions: List[str] = self.gf_server.complete(input_tokens=["5546"])
        self.assertEqual(completions, ["584"])

        completions: List[str] = self.gf_server.complete(input_tokens=["5546", "584"])
        self.assertEqual(completions, ["1815"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["5546", "584", "1815"]
        )
        self.assertEqual(completions, ["265"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["5546", "584", "1815", "265"]
        )
        self.assertEqual(completions, ["936"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["5546", "584", "1815", "265", "936"]
        )
        self.assertEqual(completions, ["3812"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["5546", "584", "1815", "265", "936", "3812"]
        )
        self.assertEqual(completions, ["518"])

        completions: List[str] = self.gf_server.complete(
            input_tokens=["5546", "584", "1815", "265", "936", "3812", "518"]
        )
        self.assertEqual(len(completions), 32)

    def test_random_decode(self):
        times = self.gf_server.random_decode(n=512, tokens2exclude={"2"})
        self.assertEqual(len(times), 512)
