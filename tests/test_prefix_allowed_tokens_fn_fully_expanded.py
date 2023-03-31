import pdb
import unittest

from tqdm import tqdm

from transformers import T5Tokenizer, BartTokenizer
from src.constrained_generation.pgf import ServerPgf
from src.config.config import ASSET_PGF_DIR




class TestPrefixAllowedTokenFn(unittest.TestCase):
    def setUp(self):
        tokenizer = BartTokenizer.from_pretrained("martinjosifoski/genie-rw")
        self.tokenizer = tokenizer
        self.pgf = ServerPgf(pgf='FullyExpandedGenieTest.pgf', port=41296, root_dir=ASSET_PGF_DIR)



        self.sentences = [
            [0],  # Start  generation
            tokenizer.encode("[")[:-1],  # Mid-subject tag
            tokenizer.encode("[s")[:-1],  # End Tag
            tokenizer.encode("[s]")[:-1],  # Start of entity
            tokenizer.encode("[s]")[:-1] + [726],  # Mid-entity
            tokenizer.encode("[s]")[:-1] + [726, 250],  # End of entity + Mid-entity
            tokenizer.encode("[s]")[:-1] + [726, 250, 1343],  # End of entity, start of rel tag
            tokenizer.encode("[s] AlAq [")[:-1],  # Mid-relation tag
            tokenizer.encode("[s] AlAq [r")[:-1],  # End relation tag
            tokenizer.encode("[s] AlAq [r]")[:-1],  # Start of relation
            tokenizer.encode("[s] AlAq [r]")[:-1] + [1248, 9],  # Mid/End of relation
            tokenizer.encode("[s] AlAq [r]")[:-1] + [1248, 9, 3113],
            # End of relation, start of obj tag
            tokenizer.encode("[s] AlAq [r]")[:-1] + [1248, 9, 3113, self._get_id("[o]", 0)],
            # Mid object tag
            tokenizer.encode("[s] AlAq [r]")[:-1]
            + [1248, 9, 3113, self._get_id("[o]", 0), self._get_id("[o]", 1)],  # End object tag
            tokenizer.encode("[s] AlAq [r] date of birth [o]")[:-1],  # Start of object
            tokenizer.encode("[s] AlAq [r] date of birth [o]")[:-1] + [726],  # Mid of object
            tokenizer.encode("[s] AlAq [r] date of birth [o]")[:-1] + [726, 250],
            # Mid + End of object
            tokenizer.encode(" [s] AlAq [r] date of birth [o]")[:-1] + [726, 250, 1343],
            # End of object
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [")[:-1],
            # Mid of end of triplet tag
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e")[:-1],
            # End of triplet tag
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e]")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s]")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s]")[:-1] + [726],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s]")[:-1] + [726, 250, 1343],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [r")[:-1],
            tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [r]")[:-1],
        ]

        self.expected_output = [
            sorted([1, self._get_id("[s]", 0)]),  # End the extraction or start a new triplet
            [self._get_id("[s]", 1)],  # s
            [self._get_id("[s]", 2)],
            [30, 726],
            [30, 250],
            sorted([1343, self._get_id("[r]", 0)]),
            [self._get_id("[r]", 0)],
            [self._get_id("[r]", 1)],
            [self._get_id("[r]", 2)],
            [16, 1248],
            sorted([744, 3113, self._get_id("[o]", 0)]),
            [self._get_id("[o]", 0)],
            [self._get_id("[o]", 1)],
            [self._get_id("[o]", 2)],
            [30, 726],
            [30, 250],
            sorted([1343, self._get_id("[e]", 0)]),
            [self._get_id("[e]", 0)],
            [self._get_id("[e]", 1)],
            [self._get_id("[e]", 2)],
            sorted([1, self._get_id("[s]", 0)]),  # End the extraction or start a new triplet
            [self._get_id("[s]", 1)],
            [self._get_id("[s]", 2)],
            [30, 726],
            [30, 250],
            [self._get_id("[r]", 0)],
            [self._get_id("[r]", 1)],
            [self._get_id("[r]", 2)],
            [16, 1248],
        ]

    def _get_id(self, string, idx):
        tokens = self.tokenizer.encode(string)

        return tokens[idx]

    def test_prefix_allowed_tokens(self):
        # for i in tqdm(range(len(self.sentences))):
        for i in tqdm([0]):
            with self.subTest(i=i):
                sent = self.sentences[i]
                # if type(sent) != torch.Tensor:
                #     sent = torch.tensor(sent)
                # pdb.set_trace()
                expected_output = self.expected_output[i]

                # self.prefix_allowed_tokens_fn = self.constrained_generation_module.get_prefix_allowed_tokens_fn()
                allowed_tokens = sorted(self.pgf.prefix_allowed_tokens(sent))
                # allowed_tokens = sorted(self.prefix_allowed_tokens_fn(0, sent))
                self.assertNotEqual(len(allowed_tokens), 0)

                for t1, t2 in zip(allowed_tokens, expected_output):
                    self.assertEqual(t1, t2)

                self.assertEqual(allowed_tokens, expected_output)


if __name__ == "__main__":
    unittest.main()
