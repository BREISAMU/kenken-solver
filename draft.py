import time
import copy
import heapq
import random

class Board:
    def __init__(self, territories, operations, n):
        self.territories = territories
        self.operations = operations
        self.n = n

class Section:
    def __init__(self, territory, operation, goal):
        self.territory = territory
        self.operation = operation
        self.goal = goal
        self.permutations = []
    
    def __lt__(self, other):
        return len(self.permutations) < len(other.permutations)
    
class Permutation:
    def __init__(self, tiles):
        self.tiles = tiles
    
    def __str__(self):
        res = "Tiles: "
        for tile in self.tiles:
            res += str(tile.value) + ","
        return res

class Tile:
    def __init__(self, y, x, value):
        self.y = y
        self.x = x
        self.value = value
    
    def __str__(self):
        return f'{self.x},{self.y} = {self.value}'

###

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
    
def make_permutations_for_section(section, k):
    domain = range(1,k+1)
    res = make_permutations(len(section.territory), operation=section.operation, goal=section.goal, domain=domain)
    return res

### Board Setup


def filter_sections(sections, dimension):
    absolutes_y = [set() for _ in range(dimension)]
    absolutes_x = [set() for _ in range(dimension)]
    cumulative_permutations = []
    absolute_permutations = [[] for _ in range(len(sections))]
    start = time.time()

    for k in range(1):
        cumulative_permutations = []
        for i in range(len(sections)):
            section = sections[i]

            real_permutations = []
            for perm in section.permutations:
                tiles = []
                valid = True

                check_y = copy.deepcopy(absolutes_y[:])
                check_x = copy.deepcopy(absolutes_x[:])

                for j in range(len(perm)):
                    t = Tile(section.territory[j][0], section.territory[j][1], perm[j])

                    x = t.x
                    y = t.y
                    value = t.value

                    if(value in check_x[x] or value in check_y[y]):
                        valid = False
                        break
                    
                    check_x[x].add(value)
                    check_y[y].add(value)

                    tiles.append(t)

                if(valid):
                    perm = Permutation(tiles)
                    real_permutations.append(perm)
                    
            cumulative_permutations.append(real_permutations)

            if(len(real_permutations) == 1):
                absolute_permutations[i] = real_permutations[0]
                for tile in real_permutations[0].tiles:
                    absolutes_x[tile.x].add(tile.value)
                    absolutes_y[tile.y].add(tile.value)
                # absolute_permutations[i] = copy.deepcopy(real_permutations[0])

    possible = [[set(range(1,dimension+1)) for _ in range(dimension)] for _ in range(dimension)]

    for m in range(len(sections)):
        if(absolute_permutations[m] != []):
            sections[m].permutations = [absolute_permutations[m]]
        else:
            sections[m].permutations = cumulative_permutations[m]
        
        real_perms = []
        for p in range(len(sections[m].permutations)):
            if(sections[m].permutations[p] != []):
                real_perms.append(sections[m].permutations[p])
        sections[m].permutations = real_perms
                

        # Used to be 10
        all_row_options = [set(range(1,dimension+1)) for _ in range(dimension+1)]
        all_col_options = [set(range(1,dimension+1)) for _ in range(dimension+1)]
        tile_count = 0
    
        for _ in range(2):
            for perm in sections[m].permutations:
                tile_count = len(perm.tiles)

                locs = []
                row_options = [set() for _ in range(dimension+1)]
                col_options = [set() for _ in range(dimension+1)]


                for tile in perm.tiles:
                    row_options[tile.x].add(tile.value)
                    col_options[tile.y].add(tile.value)

                for tile in perm.tiles:  
                    all_row_options[tile.x] = all_row_options[tile.x].intersection(row_options[tile.x])
                    all_col_options[tile.y] = all_col_options[tile.y].intersection(col_options[tile.y])

                    if ((tile.y, tile.x) not in locs):
                        locs.append((tile.y, tile.x))
                
                for n in range(dimension):
                    all_row_options[n] = all_row_options[n].intersection(row_options[n])
                    all_col_options[n] = all_col_options[n].intersection(col_options[n])

            for row_ind in range(len(all_row_options)):
                row_option_set = all_row_options[row_ind]
                if(len(row_option_set) == tile_count):
                    tiles_of_interest = set()
                    for tile_loc in locs:
                        if(tile_loc[1] == row_ind):
                            tiles_of_interest.add(tile_loc)

                    for avoid_tiles_of_interest in range(dimension):
                        if((avoid_tiles_of_interest, row_ind) not in tiles_of_interest):
                            for value in row_option_set:
                                if(value in possible[avoid_tiles_of_interest][row_ind]):
                                    possible[avoid_tiles_of_interest][row_ind].remove(value)

            for col_ind in range(len(all_col_options)):
                col_option_set = all_col_options[col_ind]
                if(len(col_option_set) == tile_count):
                    tiles_of_interest = set()
                    for tile_loc in locs:
                        if(tile_loc[0] == col_ind):
                            tiles_of_interest.add(tile_loc)

                    for avoid_tiles_of_interest in range(dimension):
                        if((col_ind, avoid_tiles_of_interest) not in tiles_of_interest):
                            for value in col_option_set:
                                if(value in possible[col_ind][avoid_tiles_of_interest]):
                                    possible[col_ind][avoid_tiles_of_interest].remove(value)
    
    for _ in range(dimension):
        for row in range(dimension):
            for col in range(dimension):
                if(len(possible[row][col]) == 1):
                    val = list(possible[row][col])[0]
                    for custom_col in range(dimension):
                        if(custom_col != col and val in possible[row][custom_col]):
                            possible[row][custom_col].remove(val)
                    for custom_row in range(dimension):
                        if(custom_row != row and val in possible[custom_row][col]):
                            possible[custom_row][col].remove(val)
        
    total_permutations = 0

    in_permutations = [[set() for _ in range(dimension)] for _ in range(dimension)]

    for l in range(len(sections)):
        section = sections[l]
        perms = section.permutations
        good_perms = []
        for perm in perms:
            valid = True
            for tile in perm.tiles:
                if(tile.value not in (possible[tile.y][tile.x])):
                    valid = False
            if(valid):
                good_perms.append(perm)
                for tile in perm.tiles:
                    in_permutations[tile.y][tile.x].add(tile.value)
        sections[l].permutations = copy.deepcopy(good_perms)
        

        total_permutations += len(sections[l].permutations)

    for _ in range(dimension):
        for i in range(len(in_permutations)):
                # perms_match_size_row_count = {}
                perms_match_size_row_locs = {}
                row = in_permutations[i]
                for j in range(len(row)):
                    unfrozen_set = row[j]
                    frozen_set = frozenset(unfrozen_set)
                    # perms_match_size_row_count[frozen_set] = perms_match_size_row_count.get(frozen_set, 0) + 1
                    perms_match_size_row_locs[frozen_set] = perms_match_size_row_locs.get(frozen_set, []) + [j]
                
                for key in perms_match_size_row_locs:
                    if(len(key) == len(perms_match_size_row_locs.get(key, []))):
                        for k in range(len(in_permutations)):
                            if(k not in perms_match_size_row_locs.get(key, [])):
                                for value in key:
                                    if(value in in_permutations[i][k]):
                                        in_permutations[i][k].remove(value)

        for i in range(len(in_permutations)):
            perms_match_size_col_locs = {}
            col = []
            for j in range(len(in_permutations)):
                col.append(in_permutations[j][i])
            
            for k in range(len(col)):
                unfrozen_set = col[k]
                frozen_set = frozenset(unfrozen_set)
                perms_match_size_col_locs[frozen_set] = perms_match_size_col_locs.get(frozen_set, []) + [k]
            
            for key in perms_match_size_col_locs:
                    if(len(key) == len(perms_match_size_col_locs.get(key, []))):
                        for m in range(len(in_permutations)):
                            if(m not in perms_match_size_col_locs.get(key, [])):
                                for value in key:
                                    if(value in in_permutations[m][i]):
                                        in_permutations[m][i].remove(value)
                                        pass

    total_permutations = 0
                                        
    for l in range(len(sections)):
        section = sections[l]
        perms = section.permutations
        good_perms = []
        for perm in perms:
            valid = True
            for tile in perm.tiles:
                if(tile.value not in (in_permutations[tile.y][tile.x])):
                    valid = False
            if(valid):
                good_perms.append(perm)
        sections[l].permutations = copy.deepcopy(good_perms)
        total_permutations += len(sections[l].permutations)

    diff = round(float(time.time() - start), 3)
    # print(f"\nFiltering complete in {diff} seconds. {total_permutations} to explore.")

def validate_board(board):
    status = "validating.... "
    valid_row = set(range(1, len(board) + 1))
    for row in board:
        if(set(row) != valid_row):
            status += "incorrect."
            return False
    
    for i in range(len(board)):
        col = set()
        for j in range(len(board)):
            col.add(board[j][i])
        if(col != valid_row):
            status += "incorrect."
            return False
    status += "correct!"
    print(status)
    return True

def sort_sections(sections):
    start = time.time()
    q = []
    for section in sections:
        heapq.heappush(q, section)

    for i in range(len(sections)):
        ele = heapq.heappop(q)
        sections[i] = ele

def validate_search(tiles, k):
    board = [[-1 for _ in range(k)] for _ in range(k)]
    for tile in tiles:
        board[tile.y][tile.x] = tile.value
    
    for i in range(len(board)):
        row_set = set()
        col_set = set()
        for j in range(len(board)):
            if(board[i][j] != -1 and board[i][j] in row_set):
                return False
            if(board[j][i] != -1 and board[j][i] in col_set):
                return False

            row_set.add(board[i][j])
            col_set.add(board[j][i])

    return True

def brute_force_v2(sections, k):
    start = time.time()
    filter_sections(sections, k)

    sort_sections(sections)
    def rec_search(tiles, board, i,start):
        if(i == len(sections)):
            for tile in tiles:
                board[tile.y][tile.x] = tile.value
            if(validate_board(board)):
                visualize(board)
                diff = round(float(time.time() - start), 3)
                print("Calculations took " + str(diff) + " second.")
                return True
        else:
            for perm in sections[i].permutations:
                pass_tiles = tiles + perm.tiles
                if(validate_search(pass_tiles, k)):
                    rec_search(pass_tiles, board, i+1, start)

    rec_search([], [[-1 for _ in range(k)] for _ in range(k)], 0, start)

def visualize(board):
    for row in board:
        row_str = ""
        for ele in row:
            if(ele >= 10):
                row_str += " " + str(ele)
            else:
                row_str += "  " + str(ele)
        print(row_str)

def is_valid(board, row, col, num, k):
    # Check if num is in the row
    if num in board[row]:
        return False
    
    # Check if num is in the column
    if num in (board[i][col] for i in range(k)):
        return False
    
    return True

def solve(sections, k):
    for i in range(len(sections)):
        sections[i].permutations = make_permutations_for_section(sections[i], k=k)
    
    brute_force_v2(sections, k=k)


section_a = Section([(0, 0), (0,1), (0,2), (0,3)], "+", 30)
section_b = Section([(0, 4), (0, 5)], "-", 1)
section_c = Section([(0, 6), (0, 7), (1, 6)], "*", 30)
section_d = Section([(0, 8), (1, 8)], "-", 5)

section_e = Section([(1, 0), (2, 0), (3, 0)], "*", 90)
section_f = Section([(1, 1), (2, 1)], "-", 3)
section_g = Section([(1, 2), (1, 3)], "-", 5)
section_h = Section([(1, 4), (1, 5)], "/", 4)
section_i = Section([(1, 7), (2, 7),  (2,8)], "+", 13)

section_j = Section([(2, 2), (2, 3), (3,2)], "+", 14)
section_k = Section([(2, 4), (3,4), (3,5)], "*", 21)
section_l = Section([(2, 5)], "=", 6)
section_m = Section([(2, 6), (3, 6), (3,7)], "+", 16)

section_n = Section([(3, 1), (4, 1)], "-", 2)
section_o = Section([(3, 3), (4, 3)], "-", 2)
section_p = Section([(3, 8), (4,8)], "+", 13)

section_q = Section([(4, 0), (5, 0)], "+", 10)
section_r = Section([(4, 2), (5, 1), (5,2)], "+", 4)
section_s = Section([(4, 4), (4, 5), (5, 4)], "*", 60)
section_t = Section([(4, 6), (4, 7)], "-", 1)

section_u = Section([(5, 3), (6,3)], "-", 1)
section_v = Section([(5, 5), (5, 6)], "+", 11)
section_w = Section([(5, 7), (5, 8)], "+", 11)

section_x = Section([(6, 0), (6, 1)], "-", 1)
section_y = Section([(6, 2), (7, 1), (7,2)], "*", 24)
section_z = Section([(6, 4), (6, 5)], "-", 8)
section_aa = Section([(6, 6), (6, 7), (7,7)], "*", 120)
section_ab = Section([(6, 8), (7,8), (8,8)], "+", 14)

section_ac = Section([(7, 0), (8,0), (8,1)], "*", 24)
section_ad = Section([(7, 3), (7, 4)], "-", 5)
section_ae = Section([(7, 5), (8, 5)], "+", 14)
section_af = Section([(7, 6), (8,6)], "-", 8)

section_ag = Section([(8, 2), (8, 3), (8,4)], "+", 12)
section_ah = Section([(8, 7)], "=", 7)

sections_9x9 = [
    section_a, section_b, section_c, section_d, section_e, section_f, section_g,
    section_h, section_i, section_j, section_k, section_l, section_m, section_n,
    section_o, section_p, section_q, section_r, section_s, section_t, section_u,
    section_v, section_w, section_x, section_y,section_z, section_aa, section_ab,
    section_ac, section_ad, section_ae, section_af, section_ag, section_ah
]

solve(sections=sections_9x9, k=9)

# section_a = Section([(0,0), (0,1), (1,0)], "*", 24) 
# section_b = Section([(0,2), (0,3)], "-", 2) 
# section_c = Section([(0,4), (0,5)], "-", 1) 
# section_d = Section([(1,1), (1,2), (1,3)], "+", 15)
# section_e = Section([(2,0), (2,1), (2,2), (3,1)], "+", 13)
# section_f = Section([(2,3), (3,3)], "-", 5)
# section_g = Section([(2,4), (2,5), (3,5)], "*", 48)
# section_h = Section([(3,0), (4,0), (5,0)], "*", 60)
# section_i = Section([(3,2)], "=", 2)
# section_j = Section([(3,4), (4,4), (5,4), (5,3)], "*", 60)
# section_k = Section([(4,1), (5,1)], "/", 3)
# section_l = Section([(4,2), (5,2)], "-", 2)
# section_m = Section([(4,3)], "=", 5)
# section_n = Section([(4,5), (5,5)], "-", 1)
# section_p = Section([(1,4), (1,5)], "-", 2)

# sections_6x6 = [
#     section_a,
#     section_b,
#     section_c,
#     section_d,
#     section_e,
#     section_f,
#     section_g,
#     section_h,
#     section_i,
#     section_j,
#     section_k,
#     section_l,
#     section_m,
#     section_n,
#     section_p,
# ]

# solve(sections=sections_6x6, k=6)