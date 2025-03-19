import time
import copy
import heapq

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


### Making permutations

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

    # print(res)
    # print(len(res))
    # print()

    return res

### Filter permutations
def filter_sections(sections):
    absolutes_y = [set() for _ in range(10)]
    absolutes_x = [set() for _ in range(10)]
    cumulative_permutations = []
    absolute_permutations = [[] for _ in range(len(sections))]
    start = time.time()

    for k in range(len(sections) * 2):
        # print("\n\n---- Iteration " + str(k) + " ----\n")
        cumulative_permutations = []
        for i in range(len(sections)):
            section = sections[i]

            # print("section_" + chr(ord("a") + i))
            real_permutations = []
            for perm in section.permutations:
                tiles = []
                valid = True

                # Limits cap to 10x10

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

            # print(str(len(real_permutations)))

            if(len(real_permutations) == 1):
                # print("hit  " + str(i))
                # print(perm)
                absolute_permutations[i] = real_permutations[0]
                for tile in real_permutations[0].tiles:
                    absolutes_x[tile.x].add(tile.value)
                    absolutes_y[tile.y].add(tile.value)
                # absolute_permutations[i] = copy.deepcopy(real_permutations[0])
                
        
        # print("\n\n----  ----\n")
    # for l in range(len(sections)):
    #     print(absolute_permutations[l])

    for m in range(len(sections)):
        
        sections[m].permutations = (cumulative_permutations[m] + [absolute_permutations[m]])
        real_perms = []
        for p in range(len(sections[m].permutations)):
            if(sections[m].permutations[p] != []):
                real_perms.append(sections[m].permutations[p])
        sections[m].permutations = real_perms
                
        # print("section_" + chr(ord('a') + m) + " " + str(len(sections[m].permutations)))

        all_row_options = [set(range(1,10)) for _ in range(10)]
        all_col_options = [set(range(1,10)) for _ in range(10)]
        tile_count = 0

    
        for perm in sections[m].permutations:
            tile_count = len(perm.tiles)

            locs = []
            row_options = [set() for _ in range(10)]
            col_options = [set() for _ in range(10)]


            for tile in perm.tiles:
                row_options[tile.y].add(tile.value)
                col_options[tile.x].add(tile.value)

            for tile in perm.tiles:  
                all_row_options[tile.y] = all_row_options[tile.y].intersection(row_options[tile.y])
                all_col_options[tile.x] = all_col_options[tile.x].intersection(col_options[tile.x])

                if ((tile.x, tile.y) not in locs):
                    locs.append((tile.x, tile.y))
            
            # all_row_options[n] = all_row_options[n].intersection(row_options[n])
            # all_col_options[n] = all_col_options[n].intersection(col_options[n])
            for n in range(10):
                all_row_options[n] = all_row_options[n].intersection(row_options[n])
                all_col_options[n] = all_col_options[n].intersection(col_options[n])

        # print(tile_count)
        for row_ind in range(len(all_row_options)):
            row_option_set = all_row_options[row_ind]
            if(len(row_option_set) == tile_count):
                tiles_of_interest = []
                for tile_loc in locs:
                    if(tile_loc[1] == row_ind):
                        tiles_of_interest.append(tile_loc)

                print(str(row_option_set) + " are in tiles " + str(tiles_of_interest) + ", therefore no other tiles in row " + str(row_ind) + " can have these values")

        for col_ind in range(len(all_col_options)):
            col_option_set = all_col_options[col_ind]
            if(len(col_option_set) == tile_count):
                tiles_of_interest = []
                for tile_loc in locs:
                    if(tile_loc[0] == col_ind):
                        tiles_of_interest.append(tile_loc)

                print(str(col_option_set) + " are in tiles " + str(tiles_of_interest) + ", therefore no other tiles in column " + str(col_ind) + " can have these values")
                    
                    

    print(f"Filtering complete in {time.time() - start} seconds")

def validate_board(board):
    status = "validating.... "
    valid_row = set(range(1, len(board) + 1))
    # print(board)
    for row in board:
        if(set(row) != valid_row):
            status += "incorrect."
            # print(status)
            return False
    
    for i in range(len(board)):
        col = set()
        for j in range(len(board)):
            col.add(board[j][i])
        if(col != valid_row):
            status += "incorrect."
            # print(status)
            return False
    status += "correct!"
    print(status)
    return True

def sort_sections(sections):
    start = time.time()
    q = []
    for section in sections:
        heapq.heappush(q, section)
    # print(q)

    for i in range(len(sections)):
        ele = heapq.heappop(q)
        sections[i] = ele
    
    print(f"Sorting complete in {time.time() - start} seconds")

def brute_force_v2(sections, k):
    filter_sections(sections)

    sort_sections(sections)

    # for section in sections:
    #     print(len(section.permutations))

    def rec_search(tiles, board, i):
        if(len(tiles) == k**2):
            # This is really fucking bad
            for tile in tiles:
                board[tile.y][tile.x] = tile.value
            if(validate_board(board)):
                visualize(board)
                return True
        else:
            for perm in sections[i].permutations:
                # print(perm)
                
                pass_tiles = tiles + perm.tiles
                rec_search(pass_tiles, board, i+1)

    rec_search([], [[-1 for _ in range(k)] for _ in range(k)], 0)

def visualize(board):
    for row in board:
        row_string = ""
        for ele in row:
            row_string += str(ele) + "  "
        print(row_string)

##### 

# sectionA = Section(territory=[(0,0), (0,1), (1,0)], operation="+", goal=6)
# sectionB = Section(territory=[(0,2)], operation="=", goal=1)
# sectionC = Section(territory=[(2,0), (2,1)], operation="-", goal=2)
# sectionD = Section(territory=[(1,1), (1,2), (2,2)], operation="+", goal=7)
# sectionA.permutations = make_permutations_for_section(sectionA, k=3)
# sectionB.permutations = make_permutations_for_section(sectionB, k=3)
# sectionC.permutations = make_permutations_for_section(sectionC, k=3)
# sectionD.permutations = make_permutations_for_section(sectionD, k=3)
# sections = [sectionA, sectionB, sectionC, sectionD]

# filter_sections(sections=sections)
# brute_force_v2(sections=sections, k=3)

sectionA = Section([(0,0), (0,1)], "/", 2)  
sectionB = Section([(1,0), (2,0)], "-", 1)  
sectionC = Section([(0,2), (1,2)], "+", 7)  
sectionD = Section([(0,3)], "=", 4)  
sectionE = Section([(1,1), (2,1)], "-", 3)  
sectionF = Section([(1,3), (2,3)], "-", 2)
sectionG = Section([(2,2), (3,2), (3,3)], "*", 4) 
sectionH = Section([(3,0), (3,1)], "-", 1) 

sections4x4 = [sectionA, sectionB, sectionC, sectionD, sectionE, sectionF, sectionG, sectionH]
# for i in range(len(sections4x4)):
#     sections4x4[i].permutations = make_permutations_for_section(sections4x4[i], k=4)

# print(sectionG.permutations)

# for section in sections4x4:



#### CURRENT SOLVER BELOW

# brute_force_v2(sections4x4, k=4)


section_a = Section([(0,0), (0,1), (0,2)], "*", 210) 
section_b = Section([(0,3), (1,3)], "-", 1) 
section_c = Section([(0,4), (0,5), (0,6)], "+", 7) 
section_d = Section([(1,0), (2,0), (3,0)], "+", 12)
section_e = Section([(1,1), (2,1)], "-", 3)
section_f = Section([(1,2), (2,2)], "/", 3)
section_g = Section([(1,4), (1,5), (1,6), (2,6)], "+", 17)
section_h = Section([(2,3), (3,3)], "+", 13)
section_i = Section([(3,4), (2,4), (2,5)], "+", 11)
section_j = Section([(3,1), (3,2), (4,2), (5,2)], "+", 19)
section_k = Section([(3,5), (4,5)], "-", 1)
section_l = Section([(3,6), (4,6)], "-", 1)
section_m = Section([(4,0), (5,0)], "*", 15)
section_n = Section([(4,1), (5,1)], "+", 3)
section_o = Section([(4,3), (5,3)], "+", 5)
section_p = Section([(4,4)], "=", 6)
section_q = Section([(6,0), (6,1)], "-", 5)
section_r = Section([(6,2), (6,3)], "-", 3)
section_s = Section([(5,4), (5,5), (6,4)], "+", 15)
section_t = Section([(6,5)], "+", 3)
section_u = Section([(6,6), (5,6)], "+", 11)

sections_7x7 = [section_a,
section_b,
section_c,
section_d,
section_e,
section_f,
section_g,
section_h,
section_i,
section_j,
section_k,
section_l,
section_m,
section_n,
section_o,
section_p,
section_q,
section_r,
section_s,
section_t,
section_u
]

start = time.time()

def solve(sections, k):
    for i in range(len(sections)):
        # print("section_" + chr(ord('a') + i) + ":")
        sections[i].permutations = make_permutations_for_section(sections[i], k=k)
        
    brute_force_v2(sections, k=k)


solve(sections=sections4x4, k=4)
solve(sections=sections_7x7, k=7)
end = time.time()
print("\nCalculations took " + str(end - start) + " second.")