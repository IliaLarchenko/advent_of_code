[Advent of code](https://adventofcode.com) is an annual coding competition where you need to solve two problems every day.

Here I share my original solutions for all problems (2022). Not all of them are optimal in terms of complexity but all of them solve the stated problems in a reasonable time. I tried to post the actual solutions that I came ups with during the contest to show how exactly I solved the problems back then given the time pressure. But I still do some code refactoring and small optimization before posting to make it more readable.

Every `N.py` file contains at least 3 functions:
- `prepare_data` - reads the input file and prepares data to be used in the solution
- `solve1` - solution of the first problem
- `solve2` - solution of the second problem

You can get the result of algorithm by running: `solve1(**prepare_data("input.txt"))`

All algorithms expect valid inputs to work correctly, e.g. if in the original problem description it is stated that the question has only one answer there should be only one valid answer.
