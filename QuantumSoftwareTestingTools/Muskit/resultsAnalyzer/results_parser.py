import ast
import json
from pathlib import Path
from os import mkdir
from os.path import basename, dirname


def parse(file_path: Path) -> None:
    """
    Parse results file into JSON data.

    Parameters
    ----------
    file_path : Path
        Path to the results file to be parsed.

    Returns
    -------
    None
        This function does not return any value.

    Notes
    -----
    This function reads the results file specified by `file_path`, breaks it
    into smaller sections corresponding to each mutant circuit, and then
    converts the data into JSON format. The JSON files are saved in a directory
    named 'json_results' within the same directory as the input file.
    """
    json_dump_options = {'sort_keys': True, 'indent': 4}

    counts_by_mutant_by_input = break_results_into_smaller_sections(file_path)

    output_dir = f"{dirname(file_path)}/json_results"
    mkdir(output_dir)

    for mutant_file_path, counts_by_input in counts_by_mutant_by_input.items():
        results_file_name = str(basename(mutant_file_path)).split('.', maxsplit=1)[0]
        with open(f"{output_dir}/{results_file_name}.json", 'x', encoding='utf-8') as file:
            json.dump(counts_by_input, fp=file, **json_dump_options)


def break_results_into_smaller_sections(file_path: Path) -> dict:
    """
    Break results file into smaller sections corresponding to each mutant circuit.

    Parameters
    ----------
    file_path : Path
        Path to the results file.

    Returns
    -------
    dict
        A dictionary containing counts by mutant by input.

    Notes
    -----
    This function reads the results file specified by `file_path`, and then
    divides it into smaller sections, each corresponding to a mutant circuit.
    It returns a dictionary where keys are mutant file paths and values are
    dictionaries containing counts by input.
    """
    counts_by_mutant_by_input = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            mutant_path, counts_by_input = extract_mutant_path(line), extract_counts_by_input(line)
            counts_by_mutant_by_input = add_counts_by_input(mutant_path, counts_by_input, counts_by_mutant_by_input)
    return counts_by_mutant_by_input


def add_counts_by_input(mutant_path: str, counts_by_input: dict,
                        counts_by_mutant_by_input: dict) -> dict:
    """
    Add counts by input dictionary into the mutation dictionary.

    Parameters
    ----------
    mutant_path : str
        Path to the mutant file.
    counts_by_input : dict
        Dictionary containing counts by input.
    counts_by_mutant_by_input : dict
        Dictionary containing counts by mutant by input.

    Returns
    -------
    dict
        Updated dictionary containing counts by mutant by input.

    Notes
    -----
    This function updates the `counts_by_mutant_by_input` dictionary with counts
    obtained from `counts_by_input` for the given `mutant_path`.
    """
    if mutant_path in counts_by_mutant_by_input:
        counts_by_mutant_by_input[mutant_path] = {
            **counts_by_mutant_by_input[mutant_path],
            **counts_by_input
        }
    else:
        counts_by_mutant_by_input[mutant_path] = counts_by_input
    return counts_by_mutant_by_input


def extract_mutant_path(line: str) -> str:
    """
    Extract mutant file path from the given line.

    Parameters
    ----------
    line : str
        Line from the results file.

    Returns
    -------
    str
        Mutant file path.

    Notes
    -----
    This function extracts the mutant file path from a line of text in the
    results file.
    """
    prefix = "The result of "
    suffix = " with input "
    i_suffix = line.find(suffix)
    return line[len(prefix):i_suffix]


def extract_counts_by_input(line: str) -> dict:
    """
    Extract output counts from the results line.

    Parameters
    ----------
    line : str
        Line from the results file.

    Returns
    -------
    dict
        Dictionary containing counts by input.

    Notes
    -----
    This function extracts the output counts from a line of text in the results file.
    """
    input_start, input_end = line.find("["), line.find("]")
    input_value = line[input_start + 1:input_end]
    counts_start, counts_end = line.find("{"), line.find("}")
    counts = ast.literal_eval(line[counts_start: counts_end + 1])
    return {input_value: counts}
