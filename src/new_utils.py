from typing import List, Union


class LiteralStr(str):
    """
    A subclass of ``str`` that is used to represent terminals in grammars.
    Instead of printing as ``dog``, it prints as ``"dog"``(with quotes).
    """

    # def __str__(self):
    #     return f'"{super().__str__()}"'

    def __new__(cls, content):
        # Add quotes to the content
        instance = super().__new__(cls, f'"{content}"')
        return instance


class Tokenization:
    def __init__(
        self, text: str, tokens: List[str], token_ids: List[int], tokenizer_name: str
    ):
        self.text = text
        self.tokens = [LiteralStr(token) for token in tokens]
        self.token_ids = [LiteralStr(str(token_id)) for token_id in token_ids]
        self.tokenizer_name = tokenizer_name


def tokenize(
    tokenizer,
    text: str,
    rm_bos=True,
    rm_eos=False,
    pseudo_prefix=False,
    start_idx=0,
    end_idx=None,
) -> Tokenization:
    PSEUDO_PREFIX = "Ж"
    if pseudo_prefix:
        text = PSEUDO_PREFIX + text
    _token_ids: List[int] = tokenizer.encode(text)
    token_ids = _post_process_token_ids(
        tokenizer, _token_ids, rm_bos=rm_bos, rm_eos=rm_eos, pseudo_prefix=pseudo_prefix
    )
    tokens = tokenizer.convert_ids_to_tokens(token_ids)

    token_ids = (
        token_ids[start_idx:end_idx] if end_idx is not None else token_ids[start_idx:]
    )
    tokens = tokens[start_idx:end_idx] if end_idx is not None else tokens[start_idx:]

    tokenization = Tokenization(
        text=text,
        tokens=tokens,
        token_ids=token_ids,
        tokenizer_name=tokenizer.name_or_path,
    )
    return tokenization


def _post_process_token_ids(
    tokenizer, token_ids: List[int], rm_bos=True, rm_eos=False, pseudo_prefix=None
) -> List[Union[int, str]]:
    "remove_bos=True, remove_eos=False"
    # N.B. case where token_ids is empty
    if len(token_ids) != 0 and token_ids[0] == tokenizer.bos_token_id and rm_bos:
        token_ids = token_ids[1:]

    if len(token_ids) != 0 and token_ids[-1] == tokenizer.eos_token_id and rm_eos:
        token_ids = token_ids[:-1]

    pseudo_prefix_token_id = (
        tokenizer.encode(pseudo_prefix, add_special_tokens=False)[0]
        if pseudo_prefix
        else None
    )

    if pseudo_prefix_token_id is not None and token_ids[0] == pseudo_prefix_token_id:
        token_ids = token_ids[1:]

    return token_ids
