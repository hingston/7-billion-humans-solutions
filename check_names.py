#!/usr/bin/env python3
import glob
import os
import re


def get_files(directories, recursive=True):
    files = []
    for d in directories:
        files_fullname = glob.glob(d + os.sep + "**", recursive=recursive)
        for f in files_fullname:
            files.append(
                dict(
                    dir=os.path.dirname(f),
                    file="" if os.path.isdir(f) else os.path.basename(f),
                )
            )
    return files


def check_year(min_year, max_year):
    def check(f):
        regex_result = re.search("Year (.*) - ", f["file"])
        try:
            year = int(regex_result.group(1))
            return year < min_year or year > max_year
        except (ValueError, AttributeError):
            return False

    return check


def check_solution_type(guilty_solutions):
    def check(f):
        try:
            solution_type = re.search(r"\((.*?)\)", f["file"]).group(1)
            return solution_type not in guilty_solutions
        except AttributeError:
            return False

    return check


def check_files(files, solution_types, min_year, max_year):
    only_files = list(filter(lambda f: f["file"] != "", files))
    txt_files = list(filter(lambda f: f["file"].endswith(".txt"), only_files))
    return {
        "Wrong extension (.txt):": list(
            filter(lambda f: not f["file"].endswith(".txt"), only_files)
        ),
        'File must start with "Year ":': list(
            filter(lambda f: not f["file"].startswith("Year "), txt_files)
        ),
        "Year must be between 2 and 68:": list(
            filter(check_year(min_year, max_year), txt_files)
        ),
        "File name must specify speed, size or both between brackets:": list(
            filter(check_solution_type(solution_types), txt_files)
        ),
    }


def print_results(results):
    results_with_issues = dict(
        filter(lambda result: len(result[1]) > 0, results.items())
    )
    if len(results_with_issues) == 0:
        print("Finished! There are no issues :)")
    else:
        for r in results_with_issues:
            print(r)
            for v in results_with_issues[r]:
                print('- "{}{}{}"'.format(v["dir"], os.sep, v["file"]))
        raise SyntaxError(
            "One or more files are not formatted correctly. Please check stdout for details!"
        )


def main():
    print_results(
        check_files(
            get_files(["Solutions99+", "Solutions50+"]),
            ["speed", "size", "both"],
            2,
            68,
        )
    )


if __name__ == "__main__":
    main()
