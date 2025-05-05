import time
import copy
import heapq
from collections import Counter

class Board:
    def __init__(self, cages, k):
        self.cages = cages
        self.k = k

class Cage:
    def __init__(self, territory, operation, goal):
        self.territory = territory
        self.operation = operation
        self.goal = goal
        self.permutations = []
    
    # MRV
    def __lt__(self, other):
        return len(self.permutations) < len(other.permutations)

class Permutation:
    def __init__(self, tiles):
        self.tiles = tiles

class Tile:
    def __init__(self, y, x, value):
        self.y = y
        self.x = x
        self.value = value


def find_multiplication_permutations(n, goal, domain):
    def rec_helper(curr, found, curr_total):
        if(len(curr) == n and curr_total == goal):
            found.add(tuple(curr))
        elif(len(curr) < n):
            for num in domain:
                rec_helper(curr[:] + [num], found, curr_total * num)
    found = set()
    rec_helper([], found, 1)
    return found

def find_addition_permutations(n, goal, domain):
    def rec_helper(curr, found, curr_total):
        if(len(curr) == n and curr_total == goal):
            found.add(tuple(curr))
        elif(len(curr) < n):
            for num in domain:
                rec_helper(curr[:] + [num], found, curr_total + num)
    found = set()
    rec_helper([], found, 0)
    return found

def make_permutations(ntiles, operation, goal, domain):
    res = set()
    if(operation == "="):
        res.add(tuple([goal]))
        return res
    elif(operation == "/"):
        for i in domain:
            for j in domain:
                if(j != i and ((i%j == 0 and i/j == goal) or (j%i == 0 and j/i == goal))):
                    res.add((i,j))
        return res
    elif(operation == "-"):
        for i in domain:
            for j in domain:
                if(j != i and i-j == goal or j-i == goal):
                    res.add((i,j))
        return res
    elif(operation == "+"):
        return find_addition_permutations(ntiles, goal, domain)
    elif(operation == "*"):
        return find_multiplication_permutations(ntiles, goal, domain)

def make_permutations_for_cage(cage, k):
    domain = range(1,k+1)
    res = make_permutations(len(cage.territory), cage.operation, cage.goal, domain)
    perms = []
    for perm in res:
        tiles = []
        for i in range(len(perm)):
            y, x = cage.territory[i]
            tiles.append(Tile(y, x, perm[i]))
        perms.append(Permutation(tiles))
    return perms

# ------------------- Heuristics -------------------

def single_square(possible):
    k = len(possible)
    for row in range(k):
        for col in range(k):
            if len(possible[row][col]) == 1:
                val = list(possible[row][col])[0]
                for c in range(k):
                    if c != col:
                        possible[row][c].discard(val)
                for r in range(k):
                    if r != row:
                        possible[r][col].discard(val)

def naked_n_tuple(possible, n):
    k = len(possible)
    for i in range(k):
        row_sets = [frozenset(possible[i][j]) for j in range(k)]
        col_sets = [frozenset(possible[j][i]) for j in range(k)]
        tuple_on_unit(row_sets, possible[i], n)
        tuple_on_unit(col_sets, [possible[j][i] for j in range(k)], n)

def tuple_on_unit(sets, tiles, n):
    counts = Counter([s for s in sets if len(s) == n])
    for valset, count in counts.items():
        if count == n:
            for i, s in enumerate(sets):
                if s != valset:
                    tiles[i].difference_update(valset)

def hidden_single(possible):
    k = len(possible)
    changed = True

    while changed:
        changed = False

        # Row check
        for row in range(k):
            count = [0 for _ in range(k + 1)]
            position = [None for _ in range(k + 1)]

            for col in range(k):
                for val in possible[row][col]:
                    count[val] += 1
                    position[val] = (row, col)

            for val in range(1, k + 1):
                if count[val] == 1:
                    r, c = position[val]
                    if possible[r][c] != {val}:
                        possible[r][c] = {val}
                        changed = True
                        # Remove from column
                        for r2 in range(k):
                            if r2 != r and val in possible[r2][c]:
                                possible[r2][c].discard(val)
                        # Remove from row
                        for c2 in range(k):
                            if c2 != c and val in possible[r][c2]:
                                possible[r][c2].discard(val)

        # Column check
        for col in range(k):
            count = [0 for _ in range(k + 1)]
            position = [None for _ in range(k + 1)]

            for row in range(k):
                for val in possible[row][col]:
                    count[val] += 1
                    position[val] = (row, col)

            for val in range(1, k + 1):
                if count[val] == 1:
                    r, c = position[val]
                    if possible[r][c] != {val}:
                        possible[r][c] = {val}
                        changed = True
                        # Remove from column
                        for r2 in range(k):
                            if r2 != r and val in possible[r2][c]:
                                possible[r2][c].discard(val)
                        # Remove from row
                        for c2 in range(k):
                            if c2 != c and val in possible[r][c2]:
                                possible[r][c2].discard(val)

def x_wing(possible):
    k = len(possible)
    for val in range(1, k+1):
        positions = []
        for row in range(k):
            cols_with_val = [col for col in range(k) if val in possible[row][col]]
            if len(cols_with_val) == 2:
                positions.append((row, tuple(cols_with_val)))
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                r1, (c1a, c1b) = positions[i]
                r2, (c2a, c2b) = positions[j]
                if {c1a, c1b} == {c2a, c2b}:
                    for r in range(k):
                        if r != r1 and r != r2:
                            possible[r][c1a].discard(val)
                            possible[r][c1b].discard(val)

def evil_twin(cages):
    for cage in cages:
        for perm in cage.permutations[:]:
            required_values = [tile.value for tile in perm.tiles]
            for i, _ in enumerate(perm.tiles):
                others = required_values[:i] + required_values[i+1:]
                if cage.operation == "+" and sum(others) > cage.goal:
                    cage.permutations.remove(perm)
                    break
                if cage.operation == "*" and product(others) > cage.goal:
                    cage.permutations.remove(perm)
                    break

def product(lst):
    result = 1
    for x in lst:
        result *= x
    return result

# ------------------- Solver Core -------------------

def count_cage_possibilites(cages):
    perm_count = 0
    for cage in cages:
            perm_count += len(cage.permutations)
    return perm_count

def filter_cages(cages, k, heuristic_to_use):
    possible = [[set() for _ in range(k)] for _ in range(k)]

    perm_count = 0
    for cage in cages:
        cage.permutations = make_permutations_for_cage(cage, k)
        for permutation in cage.permutations:
            for tile in permutation.tiles:
                possible[tile.y][tile.x].add(tile.value)
        perm_count += len(cage.permutations)
    print("\n---------------------------------------\nOriginal possibilities: " + str(perm_count))

    if "naked_n_tuple" in heuristic_to_use:
        # 2/3 are only effective n tuples
        for count in range(2,4):
            naked_n_tuple(possible, count)
        
    if "x_wing" in heuristic_to_use:
        x_wing(possible)

    if "single_square" in heuristic_to_use:
        single_square(possible)
    
    if "evil_twin" in heuristic_to_use:
        evil_twin(cages)

    if "hidden_single" in heuristic_to_use:
        hidden_single(possible)

    # Prune permutations
    perm_count = 0
    for cage in cages:
        good_permutations = []
        for permutation in cage.permutations:
            if all(tile.value in possible[tile.y][tile.x] for tile in permutation.tiles):
                good_permutations.append(permutation)
        perm_count += len(good_permutations)
        cage.permutations = good_permutations
    print("Updated possibilities: " + str(perm_count))
    

    return possible

def sort_cages(cages):
    q = []
    for cage in cages:
        heapq.heappush(q, cage)
    for i in range(len(cages)):
        cages[i] = heapq.heappop(q)

def validate_board(board):
    valid_set = set(range(1, len(board)+1))
    for row in board:
        if set(row) != valid_set:
            return False
    for col in zip(*board):
        if set(col) != valid_set:
            return False
    return True

def validate_search(tiles, k):
    board = [[-1 for _ in range(k)] for _ in range(k)]
    for tile in tiles:
        board[tile.y][tile.x] = tile.value
    for i in range(k):
        row_vals = set()
        col_vals = set()
        for j in range(k):
            if board[i][j] != -1 and board[i][j] in row_vals:
                return False
            if board[j][i] != -1 and board[j][i] in col_vals:
                return False
            row_vals.add(board[i][j])
            col_vals.add(board[j][i])
    return True

def visualize(board):
    for row in board:
        print(' '.join(f'{val:2}' for val in row))

def solve(puzzle, heuristic_to_use):
    cages = puzzle.cages
    k = puzzle.k
    filter_cages(cages, k, heuristic_to_use)
    sort_cages(cages)
    def backtrack(tiles, board, i):
        if i == len(cages):
            for tile in tiles:
                board[tile.y][tile.x] = tile.value
            if validate_board(board):
                visualize(board)
                return True
        else:
            for perm in cages[i].permutations:
                new_tiles = tiles + perm.tiles
                if validate_search(new_tiles, k):
                    if backtrack(new_tiles, copy.deepcopy(board), i+1):
                        return True
        return False
    board = [[-1 for _ in range(k)] for _ in range(k)]
    backtrack([], board, 0)
