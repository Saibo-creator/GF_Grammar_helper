import pdb
import unittest

from tqdm import tqdm

from transformers import AutoTokenizer
from src.constrained_generation.pgf import ServerPgf
from src.config.config import PGF_ASSET_DIR


class TestPrefixAllowedTokenFn(unittest.TestCase):
    def setUp(self):
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.tokenizer = tokenizer

        self.pgf = ServerPgf(pgf='SubjectCollapsedGenieT5Test.pgf', port=41296, root_dir=PGF_ASSET_DIR)



        self.sentences = [
            # [0],  # Start  generation
            [],
            [0],
            [0]+tokenizer.encode("[")[:-1],  # Mid-subject tag
            [0]+tokenizer.encode("[s")[:-1],  # End Tag
            [0]+tokenizer.encode("[s]")[:-1],  # Start of entity
            [0]+tokenizer.encode("[s] Al")[:-1],  # Mid-entity
            [0]+tokenizer.encode("[s] AlA")[:-1],  # End of entity + Mid-entity
            [0]+tokenizer.encode("[s] AlAq")[:-1],  # End of entity, start of rel tag
            [0]+tokenizer.encode("[s] AlAq [")[:-1],  # Mid-relation tag
            [0]+tokenizer.encode("[s] AlAq [r")[:-1],  # End relation tag
            [0]+tokenizer.encode("[s] AlAq [r]")[:-1],  # Start of relation
            [0]+tokenizer.encode("[s] AlAq [r] date of")[:-1],  # Mid/End of relation
            [0]+tokenizer.encode("[s] AlAq [r] date of birth")[:-1],
            # End of relation, start of obj tag
            [0]+tokenizer.encode("[s] AlAq [r] date of birth [")[:-1],
            # Mid object tag
            [0]+tokenizer.encode("[s] AlAq [r] date of birth [o")[:-1],  # End object tag
            [0]+tokenizer.encode("[s] AlAq [r] date of birth [o]")[:-1],  # Start of object
            [0]+tokenizer.encode("[s] AlAq [r] date of birth [o] Al")[:-1],  # Mid of object
            [0]+tokenizer.encode("[s] AlAq [r] date of birth [o] AlA")[:-1],
            # Mid + End of object
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq")[:-1],
            # End of object
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [")[:-1],
            # Mid of end of triplet tag
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e")[:-1],
            # End of triplet tag
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e]")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s]")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] Al")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [r")[:-1],
            [0]+tokenizer.encode(" [s] AlAq [r] date of birth [o] AlAq [e] [s] AlAq [r]")[:-1],
        ]
        self.expected_output = [
            # sorted([1, self._get_id("[s]", 0)]),  # End the extraction or start a new triplet
            [0],
            sorted([1] + self._get_token_id("[")),  # s 10975, or end the extraction with [1]
            self._get_token_id("s"),  # 29
            self._get_token_id("]"),  # 338
            sorted(self._get_token_id(" by") + self._get_token_id(" Al")),
            sorted(self._get_token_id(" by") + [self._get_id("hasA", 1)]),
            sorted(self._get_token_id("q") + self._get_token_id("[")),  # 0,1343
            self._get_token_id("["),  # 0
            self._get_token_id("r"),  # 10975
            self._get_token_id("]"),  # 338
            sorted(self._get_token_id(" is") + self._get_token_id(" date")),
            sorted(self._get_token_id("death") + self._get_token_id(" birth") + self._get_token_id("[")),  # 0, 744, 3113
            self._get_token_id("["),  # 0
            self._get_token_id("o"),  # 10975
            self._get_token_id("]"),  # 139
            sorted(self._get_token_id(" by") + self._get_token_id(" Al")),
            sorted(self._get_token_id(" by") + [self._get_id("hasA", 1)]),
            sorted(self._get_token_id("q") + self._get_token_id("[")),  # 1343,0
            self._get_token_id("["),  # 0
            sorted(self._get_token_id("r") + self._get_token_id("e")),  # 10975
            self._get_token_id("]"),  # 242
            sorted([1, self._get_id("[s]", 0)]),  # 0,1  End the extraction or start a new triplet
            self._get_token_id("s"),  # 10975
            self._get_token_id("]"),  # 29
            sorted(self._get_token_id(" by") + self._get_token_id(" Al")),
            sorted(self._get_token_id(" by") + [self._get_id("hasA", 1)]),
            self._get_token_id("["),  # 0
            self._get_token_id("r"),  # 10975
            self._get_token_id("]"),  # 338
            sorted(self._get_token_id(" is") + self._get_token_id(" date"))
        ]

    def _get_id(self, string, idx):
        tokens = self.tokenizer.encode(string)

        return tokens[idx]

    def _get_token_id(self, token):
        ids = self.tokenizer.encode(token, add_special_tokens=False)
        if ids[0]==3: # leading space
            ids= ids[1:]
        return ids

    def test_prefix_allowed_tokens(self):
        for i in tqdm(range(len(self.sentences))):
        # for i in tqdm([0]):
            with self.subTest(i=i):
                sent = self.sentences[i]

                # #TODO: Fix this
                # sent = [0]+ sent
                # if type(sent) != torch.Tensor:
                #     sent = torch.tensor(sent)
                # pdb.set_trace()
                expected_output = self.expected_output[i]

                allowed_tokens = sorted(self.pgf.prefix_allowed_tokens(sent))
                self.assertNotEqual(len(allowed_tokens), 0)

                for t1, t2 in zip(allowed_tokens, expected_output):
                    self.assertEqual(t1, t2)
                    # print(f"expected: {t2}, actual: {t1}, prefix={sent}")
                    # pdb.set_trace()
                #
                # self.assertEqual(allowed_tokens, expected_output)
                print(f"Test {i} passed:\n"
                      f"prefix tokens: {sent}\n"
                      f"allowed tokens: {allowed_tokens}\n"
                      f" expected: {expected_output}\n")

if __name__ == "__main__":
    unittest.main()
