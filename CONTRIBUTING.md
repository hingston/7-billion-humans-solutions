# Contributing

Thanks for helping collect the best 7 Billion Humans solutions! Anyone is welcome to submit an improvement, either as
a [pull request](https://help.github.com/articles/about-pull-requests/) or on
the [Steam thread](https://steamcommunity.com/app/792100/discussions/0/1739968490573286109/).

## Submitting a solution

1. Copy the solution out of the game and save it as a `.txt` file in the folder that matches how reliable it is
   (see [Which folder](#which-folder)).
2. Name the file `Year NUM - NAME (TYPE).txt`, where `NUM` is the two digit year, `NAME` is the puzzle's name and
   `TYPE` is `speed`, `size` or `both`.
3. Add or update the row in the matching README table, keeping the rows in year order.
4. Run the checks:

```bash
python check_names.py && python check_readme.py
```

Both run automatically on every pull request.

## Which folder

| Folder                  | Success rate | Contents                                                                  |
|:------------------------|:-------------|:--------------------------------------------------------------------------|
| `Solutions99+`          | 99% or more  | The main table.                                                           |
| `Solutions50+`          | 50% to 99%   | Solutions that beat the `Solutions99+` entry but do not always succeed.   |
| `SolutionsLowPercent`   | under 50%    | Solutions that beat the entries above but only succeed occasionally.      |

A less reliable solution is only listed if it is strictly better than the entry above it: fewer commands, or fewer
steps. A solution that only ties is not listed, because the more reliable solution is already the better answer.

## How size and speed are measured

**Size** is the number of commands the game counts, which is what its editor shows. Labels (`a:`), block ends
(`endif`, `endwhile`, `endfor`) and comments are free; every other line costs one command, including `else` and `end`,
and a condition split over several lines still only costs one. `check_readme.py` counts this for you and fails if the
README disagrees with the file.

**Speed** is the number of steps the game reports when the solution finishes. Solutions that rely on randomness do not
have a fixed speed, so their value is written with a `~` prefix (`~155`) for a typical run, or as a range (`10-11`)
when it varies between a couple of values.

## How solutions are ranked

The size and speed the game reports are the only numbers used. Two solutions with the same reported speed are
considered equally fast, even though one may finish a fraction of a second sooner: the game does not show that
difference, and there is no way to record it that a contributor could check. When two solutions tie on the value being
optimised, the one that is better in the other column wins, and if they tie in both then the existing entry stays.

## Solutions that have to be pasted in

Some solutions use a command the game's editor will not let you build at that level, so they can only be entered by
pasting the text in. Those rows are marked with 📋 in the README so you can tell before you try to reproduce them.

If you submit a solution that has to be pasted in, please say so in your pull request and add the marker. If you spot
a listed solution that should be marked, open an issue or a pull request; the level a command becomes available at is
easy to get wrong, so please say which command is not available and where you checked.

## Credit

The **Contributor** column records who provided the solution to this repository, which is not always the person who
first discovered it. Many of these solutions were found independently by several people, and some were posted
elsewhere first.

If you know of an earlier public posting of a solution, open an issue with a dated link to it (a Steam thread, a
Twitch VOD, a forum post) and the credit will be updated. Where a contributor knows their solution was not the first,
that is noted in a comment at the top of the solution file.

If you would rather be credited under a different name or link, say so in your pull request or open an issue.
