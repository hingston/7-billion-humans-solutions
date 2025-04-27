#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

# Define the expected file name pattern and capture groups for year and type
# Pattern: Year <year> - <description>(<type>).txt
# Group 1: year (\d+)
# Group 2: type (.*?)
FILE_PATTERN = re.compile(r"^Year (\d+) - .*\((.*?)\)\.txt$")


def get_files_recursive(directories: List[str]) -> List[Path]:
    """
    Recursively finds all files within the specified directories.

    Args:
        directories: A list of directory paths to search within.

    Returns:
        A list of pathlib.Path objects representing the files found.
    """
    all_files: List[Path] = []
    for directory in directories:
        path = Path(directory)
        if path.is_dir():
            all_files.extend([p for p in path.rglob("*") if p.is_file()])
        else:
            print(
                f"Warning: Directory '{directory}' not found or is not a directory.",
                file=sys.stderr,
            )
    return all_files


def check_files(
    files: List[Path],
    allowed_solution_types: Set[str],
    min_year: int,
    max_year: int,
) -> Dict[str, List[Path]]:
    """
    Checks a list of files against naming conventions.

    Args:
        files: A list of pathlib.Path objects to check.
        allowed_solution_types: A set of allowed solution type strings (e.g., {"speed", "size", "both"}).
        min_year: The minimum allowed year (inclusive).
        max_year: The maximum allowed year (inclusive).

    Returns:
        A dictionary mapping issue descriptions to a list of files with that issue.
    """
    issues: Dict[str, List[Path]] = {
        "Wrong extension (must be .txt):": [],
        "File name must match pattern 'Year <year> - <description>(<type>).txt':": [],
        f"Year must be between {min_year} and {max_year}:": [],
        f"Solution type must be one of {sorted(list(allowed_solution_types))}:": [],
    }

    for file_path in files:
        if file_path.suffix.lower() != ".txt":
            issues["Wrong extension (must be .txt):"].append(file_path)
            continue  # No need to perform further checks on non-.txt files
        match = FILE_PATTERN.match(file_path.name)
        if not match:
            issues[
                "File name must match pattern 'Year <year> - <description>(<type>).txt':"
            ].append(file_path)
            continue  # No year or type to extract
        year_str, solution_type = match.groups()
        try:
            year = int(year_str)
            if not (min_year <= year <= max_year):
                issues[f"Year must be between {min_year} and {max_year}:"].append(
                    file_path
                )
        except ValueError:
            pass  # Already handled by regex match failure or will be if regex allows non-digits
        if solution_type.lower() not in allowed_solution_types:
            issues[
                f"Solution type must be one of {sorted(list(allowed_solution_types))}:"
            ].append(file_path)
    return {k: v for k, v in issues.items() if v}


def print_results(results: Dict[str, List[Path]]) -> None:
    """
    Prints the results of the file checks.

    Args:
        results: A dictionary mapping issue descriptions to a list of file paths.

    Raises:
        ValueError: If one or more files are not formatted correctly.
    """
    if not results:
        print("Finished! There are no issues :)")
    else:
        print("Issues found:")
        for issue, file_list in results.items():
            print(f"\n{issue}")
            for file_path in file_list:
                print(f'- "{file_path}"')
        raise ValueError(
            "One or more files are not formatted correctly. Please check stdout for details!"
        )


def main():
    directories_to_check = ["Solutions99+", "Solutions50+", "SolutionsLowPercent"]
    allowed_types = {"speed", "size", "both"}
    min_year = 2
    max_year = 68
    all_files = get_files_recursive(directories_to_check)
    issues = check_files(all_files, allowed_types, min_year, max_year)
    print_results(issues)


if __name__ == "__main__":
    main()
