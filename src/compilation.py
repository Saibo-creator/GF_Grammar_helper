import os
import subprocess

from tqdm import tqdm

from src.config.config import NEW_GF_AUTO_GEN_GF_DIR, NEW_PGF_AUTO_GEN_DIR


def _is_grammar_crt(grammar_fpath: str) -> bool:
    """
    Check if the grammar is a concrete grammar.
    """
    with open(grammar_fpath, "r") as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith("concrete"):
            return True
    return False


def compile_grammar(
    crt_grammar_fpath: str, output_dir: str, verbose: bool = True
) -> str:
    """
    Compile the grammar to .gfo file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    cmd = f"gf -make {crt_grammar_fpath}"
    if verbose:
        print("Compiling grammar...")
        print(cmd)
    subprocess.run(cmd, shell=True, cwd=output_dir)
    pgf_fpath = crt_grammar_fpath.replace(".gf", ".pgf")

    return pgf_fpath


def compile_grammar_dir(
    grammar_dir: str, output_dir: str, verbose: bool = True, clean: bool = True
) -> None:
    """
    Compile the grammar to .gfo file.
    """
    # get all .gf files in grammar_dir
    gf_files = [f for f in os.listdir(grammar_dir) if f.endswith(".gf")]
    for gf_file in tqdm(gf_files):
        grammar_fpath = os.path.join(grammar_dir, gf_file)
        if _is_grammar_crt(grammar_fpath):
            compile_grammar(grammar_fpath, output_dir, verbose=verbose)
    if clean:
        _clean_object_files(output_dir)

    return None


def _clean_object_files(dir: str) -> None:
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".gfo"):
            os.remove(os.path.join(dir, file))


def compile_for_task(
    task: str, grammar_type: str, dataset: str, verbose: bool = True, clean: bool = True
) -> str:
    """
    Compile the grammar to .gfo file.
    """
    grammar_src_dir = os.path.join(NEW_GF_AUTO_GEN_GF_DIR, task, grammar_type, dataset)
    grammar_output_dir = os.path.join(NEW_PGF_AUTO_GEN_DIR, task, grammar_type, dataset)
    compile_grammar_dir(
        grammar_src_dir, grammar_output_dir, verbose=verbose, clean=clean
    )

    return grammar_output_dir


# Usage:
# pgf_file_path = CompilerWrapper.compile_grammar("/path/to/grammar.gf", "/path/to/output_dir")
