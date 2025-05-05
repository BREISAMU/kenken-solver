
# # ------------------- Example Puzzles -------------------

# cage_a = Cage([(0, 0), (0,1), (0,2), (0,3)], "+", 30)
# cage_b = Cage([(0, 4), (0, 5)], "-", 1)
# cage_c = Cage([(0, 6), (0, 7), (1, 6)], "*", 30)
# cage_d = Cage([(0, 8), (1, 8)], "-", 5)

# cage_e = Cage([(1, 0), (2, 0), (3, 0)], "*", 90)
# cage_f = Cage([(1, 1), (2, 1)], "-", 3)
# cage_g = Cage([(1, 2), (1, 3)], "-", 5)
# cage_h = Cage([(1, 4), (1, 5)], "/", 4)
# cage_i = Cage([(1, 7), (2, 7),  (2,8)], "+", 13)

# cage_j = Cage([(2, 2), (2, 3), (3,2)], "+", 14)
# cage_k = Cage([(2, 4), (3,4), (3,5)], "*", 21)
# cage_l = Cage([(2, 5)], "=", 6)
# cage_m = Cage([(2, 6), (3, 6), (3,7)], "+", 16)

# cage_n = Cage([(3, 1), (4, 1)], "-", 2)
# cage_o = Cage([(3, 3), (4, 3)], "-", 2)
# cage_p = Cage([(3, 8), (4,8)], "+", 13)

# cage_q = Cage([(4, 0), (5, 0)], "+", 10)
# cage_r = Cage([(4, 2), (5, 1), (5,2)], "+", 4)
# cage_s = Cage([(4, 4), (4, 5), (5, 4)], "*", 60)
# cage_t = Cage([(4, 6), (4, 7)], "-", 1)

# cage_u = Cage([(5, 3), (6,3)], "-", 1)
# cage_v = Cage([(5, 5), (5, 6)], "+", 11)
# cage_w = Cage([(5, 7), (5, 8)], "+", 11)

# cage_x = Cage([(6, 0), (6, 1)], "-", 1)
# cage_y = Cage([(6, 2), (7, 1), (7,2)], "*", 24)
# cage_z = Cage([(6, 4), (6, 5)], "-", 8)
# cage_aa = Cage([(6, 6), (6, 7), (7,7)], "*", 120)
# cage_ab = Cage([(6, 8), (7,8), (8,8)], "+", 14)

# cage_ac = Cage([(7, 0), (8,0), (8,1)], "*", 24)
# cage_ad = Cage([(7, 3), (7, 4)], "-", 5)
# cage_ae = Cage([(7, 5), (8, 5)], "+", 14)
# cage_af = Cage([(7, 6), (8,6)], "-", 8)

# cage_ag = Cage([(8, 2), (8, 3), (8,4)], "+", 12)
# cage_ah = Cage([(8, 7)], "=", 7)

# cages_9x9 = [
#     cage_a, cage_b, cage_c, cage_d, cage_e, cage_f, cage_g,
#     cage_h, cage_i, cage_j, cage_k, cage_l, cage_m, cage_n,
#     cage_o, cage_p, cage_q, cage_r, cage_s, cage_t, cage_u,
#     cage_v, cage_w, cage_x, cage_y,cage_z, cage_aa, cage_ab,
#     cage_ac, cage_ad, cage_ae, cage_af, cage_ag, cage_ah
# ]
# all_permutations = ["single_square", "naked_n_tuple", "hidden_single", "x_wing", "evil_twin"]

# def solve_with_permutation_combos(cages, k, all_permutations):
#     total = 0.0
#     div = 0.0

#     start = time.time()
#     solve(cages, k, [])
#     diff = round(float(time.time() - start), 3)
#     print("Calculations took " + str(diff) + " second without any heuristics.\n")

#     for i in range(len(all_permutations)):
#         start = time.time()
#         solve(cages, k, [all_permutations[i]])
#         diff = round(float(time.time() - start), 3)
#         total += diff
#         div += 1
#         print("Calculations took " + str(diff) + " using: " + all_permutations[i] + ".")
    
#     print("\nAverage time:  " + str(round(total / div, 3)))


# def solve_with_all_permutation(puzzle, all_permutations):
#     start = time.time()
#     solve(puzzle, all_permutations)
#     diff = round(float(time.time() - start), 20)
#     print("Calculations took " + str(diff) + " using all heuristics.")

# def solve_with_specific_permutation(puzzle, specific):
#     start = time.time()
#     solve(puzzle, [specific])
#     diff = round(float(time.time() - start), 20)
#     print("Calculations took " + str(diff) + " using " + specific + ".")

# b = Board(cages_9x9, 9)

# sectionA = Cage([(0,0), (0,1)], "/", 2)  
# sectionB = Cage([(1,0), (2,0)], "-", 1)  
# sectionC = Cage([(0,2), (1,2)], "+", 7)  
# sectionD = Cage([(0,3)], "=", 4)  
# sectionE = Cage([(1,1), (2,1)], "-", 3)  
# sectionF = Cage([(1,3), (2,3)], "-", 2)
# sectionG = Cage([(2,2), (3,2), (3,3)], "*", 4) 
# sectionH = Cage([(3,0), (3,1)], "-", 1) 

# sections4x4 = [sectionA, sectionB, sectionC, sectionD, sectionE, sectionF, sectionG, sectionH]
# b4 = Board(sections4x4, 4)

# section_a = Cage([(0,0), (0,1), (0,2)], "+", 6) 
# section_b = Cage([(0,3), (0,4), (1,3), (2,3)], "*", 40) 
# section_c = Cage([(1,0), (1,1)], "-", 3) 
# section_d = Cage([(1,2), (2,2), (3,2)], "*", 60)
# section_e = Cage([(1,4), (2,4)], "-", 1)
# section_f = Cage([(2,0), (2,1)], "-", 2)
# section_g = Cage([(3,0), (4,0)], "/", 2)
# section_h = Cage([(3,1), (4,1), (4,2)], "*", 10)
# section_i = Cage([(3,3), (3,4)], "-", 4)
# section_j = Cage([(4,3), (4,4)], "-", 1)

# sections_5x5 = [section_a,
# section_b,
# section_c,
# section_d,
# section_e,
# section_f,
# section_g,
# section_h,
# section_i,
# section_j,
# ]

# b5 = Board(sections_5x5, 5)


# def run_all(b, all_heuristics):
#     for heuristic in all_heuristics:
#         solve_with_specific_permutation(b, heuristic)
#     solve_with_all_permutation(b,all_heuristics)


# section_a = Cage([(0,0), (0,1), (1,0)], "*", 24) 
# section_b = Cage([(0,2), (0,3)], "-", 2) 
# section_c = Cage([(0,4), (0,5)], "-", 1) 
# section_d = Cage([(1,1), (1,2), (1,3)], "+", 15)
# section_e = Cage([(2,0), (2,1), (2,2), (3,1)], "+", 13)
# section_f = Cage([(2,3), (3,3)], "-", 5)
# section_g = Cage([(2,4), (2,5), (3,5)], "*", 48)
# section_h = Cage([(3,0), (4,0), (5,0)], "*", 60)
# section_i = Cage([(3,2)], "=", 2)
# section_j = Cage([(3,4), (4,4), (5,4), (5,3)], "*", 60)
# section_k = Cage([(4,1), (5,1)], "/", 3)
# section_l = Cage([(4,2), (5,2)], "-", 2)
# section_m = Cage([(4,3)], "=", 5)
# section_n = Cage([(4,5), (5,5)], "-", 1)
# section_p = Cage([(1,4), (1,5)], "-", 2)

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


# b6 = Board(sections_6x6, 6)
# # run_all(b4, all_permutations)
# # run_all(b6, all_permutations)
# # solve_with_all_permutation(b, all_permutations)
# # solve_with_specific_permutation(cages_9x9, 9, "")
# # solve_with_specific_permutation(cages_9x9, 9, "hidden_single")

# cage_a = Cage([(0, 0), (0,1), (0,2), (0,3)], "+", 30)
# cage_b = Cage([(0, 4), (0, 5)], "-", 1)
# cage_c = Cage([(0, 6), (0, 7), (1, 6)], "*", 30)
# cage_d = Cage([(0, 8), (1, 8)], "-", 5)

# cage_e = Cage([(1, 0), (2, 0), (3, 0)], "*", 90)
# cage_f = Cage([(1, 1), (2, 1)], "-", 3)
# cage_g = Cage([(1, 2), (1, 3)], "-", 5)
# cage_h = Cage([(1, 4), (1, 5)], "/", 4)
# cage_i = Cage([(1, 7), (2, 7),  (2,8)], "+", 13)

# cage_j = Cage([(2, 2), (2, 3), (3,2)], "+", 14)
# cage_k = Cage([(2, 4), (3,4), (3,5)], "*", 21)
# cage_l = Cage([(2, 5)], "=", 6)
# cage_m = Cage([(2, 6), (3, 6), (3,7)], "+", 16)

# cage_n = Cage([(3, 1), (4, 1)], "-", 2)
# cage_o = Cage([(3, 3), (4, 3)], "-", 2)
# cage_p = Cage([(3, 8), (4,8)], "+", 13)

# cage_q = Cage([(4, 0), (5, 0)], "+", 10)
# cage_r = Cage([(4, 2), (5, 1), (5,2)], "+", 4)
# cage_s = Cage([(4, 4), (4, 5), (5, 4)], "*", 60)
# cage_t = Cage([(4, 6), (4, 7)], "-", 1)

# cage_u = Cage([(5, 3), (6,3)], "-", 1)
# cage_v = Cage([(5, 5), (5, 6)], "+", 11)
# cage_w = Cage([(5, 7), (5, 8)], "+", 11)

# cage_x = Cage([(6, 0), (6, 1)], "-", 1)
# cage_y = Cage([(6, 2), (7, 1), (7,2)], "*", 24)
# cage_z = Cage([(6, 4), (6, 5)], "-", 8)
# cage_aa = Cage([(6, 6), (6, 7), (7,7)], "*", 120)
# cage_ab = Cage([(6, 8), (7,8), (8,8)], "+", 14)

# cage_ac = Cage([(7, 0), (8,0), (8,1)], "*", 24)
# cage_ad = Cage([(7, 3), (7, 4)], "-", 5)
# cage_ae = Cage([(7, 5), (8, 5)], "+", 14)
# cage_af = Cage([(7, 6), (8,6)], "-", 8)

# cage_ag = Cage([(8, 2), (8, 3), (8,4)], "+", 12)
# cage_ah = Cage([(8, 7)], "=", 7)

# cages_9x9 = [
#     cage_a, cage_b, cage_c, cage_d, cage_e, cage_f, cage_g,
#     cage_h, cage_i, cage_j, cage_k, cage_l, cage_m, cage_n,
#     cage_o, cage_p, cage_q, cage_r, cage_s, cage_t, cage_u,
#     cage_v, cage_w, cage_x, cage_y,cage_z, cage_aa, cage_ab,
#     cage_ac, cage_ad, cage_ae, cage_af, cage_ag, cage_ah
# ]
# all_permutations = ["single_square", "naked_n_tuple", "hidden_single", "x_wing", "evil_twin"]
# b = Board(cages_9x9, 9)

# section_a = Cage([(0,0), (0,1), (0,2)], "+", 18) 
# section_b = Cage([(0,3), (0,4)], "/", 2) 
# section_c = Cage([(0,5), (1,5)], "-", 2) 
# section_d = Cage([(0,6), (1,6)], "-", 2)
# section_e = Cage([(1,0), (2,0)], "*", 28)
# section_f = Cage([(1,1), (1,2), (2,1)], "+", 11)
# section_g = Cage([(1,3)], "=", 1)
# section_h = Cage([(1,4), (2,4)], "+", 8)
# section_i = Cage([(2,2), (2,3)], "-", 4) #
# section_j = Cage([(2,5), (3,5), (4,5)], "*", 126) #
# section_k = Cage([(2,6), (3,6), (4,6)], "*", 56)
# section_l = Cage([(3,0), (4,0), (5,0)], "*", 10)
# section_m = Cage([(3,1), (3,2)], "-", 1) #
# section_n = Cage([(3,3), (3,4)], "-", 1)
# section_o = Cage([(4,1), (5,1)], "+", 5)
# section_p = Cage([(4,2), (4,3)], "-", 5)
# section_q = Cage([(4,4), (5,4)], "+", 11) #
# section_r = Cage([(5,2), (5,3)], "-", 1) #
# section_s = Cage([(6,0), (6,1), (6,2)], "+", 12)#
# section_t = Cage([(6,3), (6,4)], "-", 2)#
# section_u = Cage([(5,5), (6,5)], "-", 4)#
# section_v = Cage([(5,6), (6,6)], "-", 5)#


# book_7x7 = [
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
#     section_o,
#     section_p,
#     section_q,
#     section_r,
#     section_s,
#     section_t,
#     section_u,
#     section_v,
# ]

# b = Board(book_7x7, 7)

# run_all(b, all_permutations)