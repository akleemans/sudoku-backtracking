# sudoku-backtracking

Sudoku solver with backtracking, without recursion.

The solver works with a stack, a depth first search (DFS) is performed with "minimum remaining values" heuristic.
It is not optimized but will still perform decently, see benchmarks below.

Uses tkinter to show a visualization (with candidates):

![A partially filled Sudoku](sudoku.png)

Inspired by [Ali Spittel's post](https://medium.com/free-code-camp/coming-back-to-old-problems-how-i-finally-wrote-a-sudoku-solving-algorithm-3b371e6c63bd) and the amazing Peter Norvig essay ["Solving Every Sudoku Puzzle"](https://norvig.com/sudoku.html).

### Run

To start solving, just run:

    python3 main.py
    
This will solve all the Sudokus listed below.

You can specify if a single Sudoku should be solved (`solve_single`) or a all from a file (`solve_all`):

    solve_single('7.18.43.......2.....453..7.6.....7..1...9...5..8.....38...195....23........6.89.4')
    solve_all('magictour_easy.csv')

### Sudokus

Some Sudokus for testing and benchmarking can be found in the `Sudoku` folder:

* `magictour_easy.csv`: 1011 easy puzzles (without solutions), [source](http://magictour.free.fr/msk_009)
* `magictour_hard.csv`: 95 hard puzzles (without solutions), [source](http://magictour.free.fr/top95)
* `menneske_random.csv`: 90 puzzles from all difficulties (with solutions), [source](http://www.menneske.no/sudoku/eng/random.html)
* `norvig_hardest.csv`: 10 "hardest" puzzles, [source](https://norvig.com/hardest.txt)

### Benchmarking

On my 2015 MacBook Pro (2.7 GHz Dual-Core Intel Core i5), the solver performs like this:

* `magictour_easy.csv`: 1011 puzzles in 28.26 seconds (0.028s per puzzle) 
* `magictour_hard.csv`: 95 puzzles in 20.68 seconds (0.218s per puzzle)
* `menneske_random.csv`: 90 puzzles in 2.35 seconds (0.026s per puzzle)
* `norvig_hardest.csv`: 10 puzzles in 0.44 seconds (0.044 per puzzle)
