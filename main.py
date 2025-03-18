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
    
class Permutation:
    def __init__(self, tiles):
        self.tiles = tiles
    
    def __str__(self):
        res = "Tiles:\n"
        for tile in self.tiles:
            res += str(tile) + "\n"
        return res

class Tile:
    def __init__(self, y, x, value):
        self.y = y
        self.x = x
        self.value = value
    
    def __str__(self):
        return f'{self.x},{self.y} = {self.value}'


### Making permutations

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
    
def make_permutations_for_section(section, domain=range(1,4)):
    res = make_permutations(len(section.territory), operation=section.operation, goal=section.goal, domain=domain)
    return res

###

sectionA = Section(territory=[(0,0), (0,1), (1,0)], operation="+", goal=6)
sectionB = Section(territory=[(0,2)], operation="=", goal=1)
sectionC = Section(territory=[(2,0), (2,1)], operation="-", goal=2)
sectionD = Section(territory=[(1,1), (1,2), (2,2)], operation="+", goal=7)

sectionA.permutations = make_permutations_for_section(sectionA)
sectionB.permutations = make_permutations_for_section(sectionB)
sectionC.permutations = make_permutations_for_section(sectionC)
sectionD.permutations = make_permutations_for_section(sectionD)

sections = [sectionA, sectionB, sectionC, sectionD]

### Filter permutations

cumulative_permutations = []
for i in range(len(sections)):
    section = sections[i]
    real_permutations = []
    for perm in section.permutations:
        tiles = []
        for i in range(len(perm)):
            t = Tile(section.territory[i][0], section.territory[i][1], perm[i])
            tiles.append(t)
        perm = Permutation(tiles)
        real_permutations.append(perm)
    cumulative_permutations.append(real_permutations)

for i in range(len(sections)):
    sections[i].permutations = cumulative_permutations[i]
    
board = [[-1 for _ in range(3)] for _ in range(3)]

def validate_board(board):
    valid_row = set(range(1, len(board) + 1))
    for row in board:
        if(set(row) != valid_row):
            return False
    
    for i in range(len(board)):
        col = set()
        for j in range(len(board)):
            col.add(board[j][i])
        if(col != valid_row):
            return False

    return True

def brute_force():
    for permA in sectionA.permutations:
        for permB in sectionB.permutations:
            for permC in sectionC.permutations:
                for permD in sectionD.permutations:
                    allTiles = permA.tiles + permB.tiles + permC.tiles + permD.tiles
                    for tile in allTiles:
                        board[tile.y][tile.x] = tile.value
                    
                    if(validate_board(board)):
                        visualize(board)
                        return True
    return False

def visualize(board):
    for row in board:
        row_string = ""
        for ele in row:
            row_string += str(ele) + "  "
        print(row_string)


brute_force()
