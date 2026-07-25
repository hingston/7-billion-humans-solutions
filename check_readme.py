#!/usr/bin/env python3
"""Check that the tables in README.md agree with the solution files."""

import re
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Set

REPO_ROOT = Path(__file__).parent
README = REPO_ROOT / "README.md"
BLOB_PREFIX = "https://github.com/hingston/7-billion-humans-solutions/blob/master/"

# Maps a README section heading to the folder its rows must link to.
SECTION_DIRECTORIES: Dict[str, str] = {
    "+99% Solutions": "Solutions99+",
    "+50% Solutions": "Solutions50+",
    "<50% Solutions": "SolutionsLowPercent",
}

SECTION_PATTERN = re.compile(r"^###### (.*)$")
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\((.*\.txt)\)")
FILE_TYPE_PATTERN = re.compile(r"\((speed|size|both)\)\.txt$", re.IGNORECASE)
MARKERS = "❌✔➕➖📋"

# Statements that the game does not count towards a solution's size.
BLOCK_END_PATTERN = re.compile(r"^end(if|while|for)$")
LABEL_PATTERN = re.compile(r"^[A-Za-z_]\w*:$")
COMMENT_COMMAND_PATTERN = re.compile(r"^comment \d+$")
CONDITION_PATTERN = re.compile(r"^(if|while)\b")
ELSE_PATTERN = re.compile(r"^else:?$")


class Row(NamedTuple):
    """One solution row of one of the README tables."""

    line_number: int
    section: str
    year: str
    name: str
    path: Optional[Path]
    url: str
    size: str
    speed: str


def read_statements(path: Path) -> List[str]:
    """
    Splits a solution file into the statements the game counts as its size.

    Blank lines, `-- comment --` headers and the trailing `DEFINE COMMENT` payloads are dropped, and a condition
    spread over several lines is joined back into a single statement.

    Args:
        path: The solution file to read.

    Returns:
        A list of statements, one per line of code as the game's editor shows it.
    """
    statements: List[str] = []
    pending = ""
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("--"):
            continue
        if line.startswith("DEFINE "):
            break  # the comment/label payloads at the end of a file are not code
        pending = f"{pending} {line}" if pending else line
        if CONDITION_PATTERN.match(pending) and not pending.endswith(":"):
            continue  # a condition continues on the next line
        statements.append(pending)
        pending = ""
    if pending:
        statements.append(pending)
    return statements


def is_free(statement: str) -> bool:
    """
    Reports whether a statement is one the game does not charge a command for.

    Args:
        statement: A single statement of a solution.

    Returns:
        True if the statement does not count towards the solution's size.
    """
    if ELSE_PATTERN.match(statement):
        return False  # `else` looks like a label but does cost a command
    return bool(
        LABEL_PATTERN.match(statement)
        or BLOCK_END_PATTERN.match(statement)
        or COMMENT_COMMAND_PATTERN.match(statement)
    )


def solution_size(path: Path) -> int:
    """
    Counts the commands in a solution, the way the game's size counter does.

    Labels, block ends (`endif`, `endwhile`, `endfor`) and `comment` commands are free; everything else, including
    `else` and `end`, costs one command.

    Args:
        path: The solution file to measure.

    Returns:
        The number of commands in the solution.
    """
    return sum(1 for statement in read_statements(path) if not is_free(statement))


def cell_value(cell: str) -> Optional[int]:
    """
    Reads the number out of a Size or Speed table cell.

    Args:
        cell: The cell's text, which may be bold and may carry a marker, a `~` or a range such as `10-11`.

    Returns:
        The number, taking the lowest value of a range, or None if the cell holds no plain number.
    """
    text = cell.replace("**", "")
    for marker in MARKERS:
        text = text.replace(marker, "")
    text = text.strip().lstrip("~").strip()
    match = re.match(r"^(\d+)(-\d+)?$", text)
    return int(match.group(1)) if match else None


def is_bold(cell: str) -> bool:
    """
    Reports whether a table cell is bold, which marks the value a solution is optimised for.

    Args:
        cell: The cell's text.

    Returns:
        True if the cell is bold.
    """
    return "**" in cell


def url_to_path(url: str) -> Optional[Path]:
    """
    Turns a README link into the path of the file it points at.

    Args:
        url: The link's target.

    Returns:
        The path the link points at, or None if the link is not a link into this repository.
    """
    if not url.startswith(BLOB_PREFIX):
        return None
    return REPO_ROOT / urllib.parse.unquote(url[len(BLOB_PREFIX) :])


def parse_readme() -> List[Row]:
    """
    Reads every solution row out of the README's tables.

    Returns:
        A list of rows, in the order they appear in the README.
    """
    rows: List[Row] = []
    section = None
    for line_number, line in enumerate(
        README.read_text(encoding="utf-8").splitlines(), 1
    ):
        heading = SECTION_PATTERN.match(line)
        if heading:
            section = (
                heading.group(1) if heading.group(1) in SECTION_DIRECTORIES else None
            )
            continue
        if section is None or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] == "Year" or set(cells[0]) <= set(":- "):
            continue  # heading or separator row
        link = LINK_PATTERN.search(cells[1])
        if not link:
            continue
        rows.append(
            Row(
                line_number=line_number,
                section=section,
                year=cells[0],
                name=link.group(1),
                path=url_to_path(link.group(2)),
                url=link.group(2),
                size=cells[3],
                speed=cells[4],
            )
        )
    return rows


def check_rows(rows: List[Row]) -> List[str]:
    """
    Checks every README row against the file it links to.

    Args:
        rows: The rows read from the README.

    Returns:
        A list of problem descriptions, empty if every row is correct.
    """
    problems: List[str] = []
    for row in rows:
        where = f'README.md:{row.line_number} "{row.year} {row.name}"'
        if row.path is None:
            problems.append(
                f"{where}: link does not point into this repository: {row.url}"
            )
            continue
        if not row.path.is_file():
            problems.append(
                f"{where}: link points at a file that does not exist: {row.url}"
            )
            continue
        expected_directory = SECTION_DIRECTORIES[row.section]
        if row.path.parent.name != expected_directory:
            problems.append(
                f"{where}: is listed under {row.section} but links to {row.path.parent.name}, "
                f"expected {expected_directory}"
            )
            continue
        size = cell_value(row.size)
        actual_size = solution_size(row.path)
        if size is None:
            problems.append(f"{where}: Size column is not a number: {row.size}")
        elif size != actual_size:
            problems.append(
                f"{where}: Size column says {size} but the solution has {actual_size} commands"
            )
        file_type_match = FILE_TYPE_PATTERN.search(row.path.name)
        if not file_type_match:
            continue  # check_names.py reports the bad file name
        file_type = file_type_match.group(1).lower()
        expected_bold = {
            "size": (True, False),
            "speed": (False, True),
            "both": (True, True),
        }[file_type]
        if (is_bold(row.size), is_bold(row.speed)) != expected_bold:
            problems.append(
                f"{where}: is a ({file_type}) solution, so only the "
                f"{'Size and Speed columns' if file_type == 'both' else file_type.capitalize() + ' column'} "
                "should be bold"
            )
    return problems


def check_files_are_listed(rows: List[Row]) -> List[str]:
    """
    Checks that every solution file is listed in the README exactly once.

    Args:
        rows: The rows read from the README.

    Returns:
        A list of problem descriptions, empty if every file is listed exactly once.
    """
    problems: List[str] = []
    listed: Set[Path] = set()
    for row in rows:
        if row.path is None:
            continue
        if row.path in listed:
            problems.append(
                f"README.md:{row.line_number}: {row.path.name} is listed more than once"
            )
        listed.add(row.path)
    for directory in SECTION_DIRECTORIES.values():
        for path in sorted((REPO_ROOT / directory).glob("*.txt")):
            if path not in listed:
                problems.append(f'"{directory}/{path.name}" is not listed in README.md')
    return problems


def check_lower_percent_rows_are_better(rows: List[Row]) -> List[str]:
    """
    Checks that a less reliable solution is only listed if it beats the more reliable one.

    Args:
        rows: The rows read from the README.

    Returns:
        A list of problem descriptions, empty if every row earns its place.
    """
    problems: List[str] = []
    best: Dict[str, Dict[str, int]] = {}
    for row in rows:
        columns = {
            column: cell_value(cell)
            for column, cell in (("Size", row.size), ("Speed", row.speed))
            if is_bold(cell)
        }
        year_best = best.setdefault(row.year, {})
        comparable = {
            column: (value, year_best[column])
            for column, value in columns.items()
            if value is not None and column in year_best
        }
        if (
            row.section != "+99% Solutions"
            and comparable
            and not any(value < previous for value, previous in comparable.values())
        ):
            beaten = ", ".join(
                f"{column} {value} against {previous}"
                for column, (value, previous) in sorted(comparable.items())
            )
            problems.append(
                f'README.md:{row.line_number} "{row.year} {row.name}": does not beat the more reliable solution '
                f"already listed ({beaten}), so it does not belong in {row.section}"
            )
        for column, value in columns.items():
            if value is not None and value < year_best.get(column, value + 1):
                year_best[column] = value
    return problems


def main() -> None:
    """
    Checks the README against the solution files and exits non-zero if anything is wrong.
    """
    rows = parse_readme()
    problems = (
        check_rows(rows)
        + check_files_are_listed(rows)
        + check_lower_percent_rows_are_better(rows)
    )
    if not problems:
        print(f"Finished! Checked {len(rows)} solutions and there are no issues :)")
        return
    print("Issues found:\n")
    for problem in problems:
        print(f"- {problem}")
    sys.exit(1)


if __name__ == "__main__":
    main()
