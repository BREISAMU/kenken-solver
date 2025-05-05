## Ken-Ken Solver
This repository contains code used in a research project for CSCI 4511W: Introduction to Artificial Intelligence, [as well as copy of the paper itself](/Samuel_Breider_KenKen_Report.pdf). 

## Abstract
A player can intuitively identify a set of baseline patterns when solving KenKen
puzzles. This report aims to identify these patterns, namely Single Square,
Naked N Tuple, X-Wing, Evil Twin, and Hidden Single, and codify them into
custom heuristics. These heuristics are then compared to determine which has
the greatest effect on search space size and solve time. When solving this puzzle,
KenKen boards are framed as a standard constraint satisfaction problem (CSP).
Each tile on the board has its own domain of number values, and each cage has
its own domain of tile permutations. The overall search space is quantified by
the number of possible cage permutations on the board, rather than the number
of possible values. The approach was to solve five KenKen puzzles of various dimensions. For
each, assorted orderings and combinations of pruning heuristics were tested to
measure their effectiveness in reducing the search space. Through this, it was
found that Naked N Tuple and Single Square had a significantly large effect
on search space size, whereas instances of the other patterns were far more
sparse. All sparsely used or unused heuristics shared a key characteristic: they
depended on partial pruning already performed by the player during puzzle
solving. This suggests that the initial pruning done by a program is extensive
enough to render these patterns less relevant in practice.
