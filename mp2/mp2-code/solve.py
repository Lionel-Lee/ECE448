# -*- coding: utf-8 -*-
import numpy as np

def solve(board, pents):
    pents_num = len(pents)
    board = 1 - board           #swap 0 and 1, 0 for available place
    # result_list = []
    # # result_list = solve_helper(cur_board, pents, 0, result_list)[0]
    # return result_list
    board_unavailble_pos = np.where(board.ravel())
    for pos in board_unavailble_pos:
        pos += pents_num 

    board_mat = []
    pent_coord_mat = []
    for i in range(pents_num):
        board_list, pent_coord_list = pent_possible_place(board, pents[i])
        for cur_board in board_list:
            cur_board = np.append(np.zeros(pents_num), cur_board)
            cur_board = np.delete(cur_board, board_unavailble_pos)
            cur_board[i] = 1
            board_mat.append(cur_board)
        pent_coord_mat.extend(pent_coord_list)

    board_mat = np.array(board_mat)
    # print(board_mat.shape)
    board_mat[board_mat > 0] = 1
    solution_list = pent_cover_solver(board_mat)

    solutions = []
    for i in solution_list:
        pent, coord = pent_coord_mat[i][0], (pent_coord_mat[i][1],pent_coord_mat[i][2])
        solutions.append((pent, coord))
    return solutions

# def solve_helper(cur_board, pents, pent_idx, result_list):
#     print(cur_board)
#     if(pent_idx == len(pents)):
#         return result_list, True
#     pent = pents[pent_idx]
#     for x in range(cur_board.shape[0]):
#         for y in range(cur_board.shape[1]):
#             coord = (x,y)
#             # if  ((x==0 or cur_board[x-1][y] > 0) and \
#             #     (y==0 or cur_board[x][y-1] > 0) and    \
#             #     (x==cur_board.shape[0]-1 or cur_board[x+1][y] > 0) and \
#             #     (y==cur_board.shape[1]-1 or cur_board[x][y+1] > 0)):
#             #         return result_list, False
#             for flip in range(2):
#                 if(flip):
#                     p = np.flip(pent, 1)
#                 else:
#                     p = np.copy(pent)
#                 for _ in range(4):
#                     p = np.rot90(p)
#                     sol_board = np.copy(cur_board)
#                     if(add_pentomino(sol_board, p, coord, pents)):
#                         result = (p, coord)
#                         result_list, success = solve_helper(sol_board, pents, pent_idx+1, result_list+[result])
#                         if (success):
#                             return result_list, True
#     return result_list, False

# def add_pentomino(board, pent, coord, valid_pents=None):
#     if ((coord[0] + pent.shape[0] - 1 >= board.shape[0]) or (coord[1] + pent.shape[1] - 1 >= board.shape[1])):
#         return False
#     for row in range(pent.shape[0]):
#         for col in range(pent.shape[1]):
#             if pent[row][col] != 0:
#                 if board[coord[0]+row][coord[1]+col] != 0: # Overlap
#                     return False
#                 else:
#                     board[coord[0]+row][coord[1]+col] = pent[row][col]
#     return True

def pent_possible_place(board, pent):       #generate all possible placement for a single pent
    board_list = []
    pent_pos_list = []
    for p in pent_trans_repo(pent):
        h, w = p.shape
        for i in range(board.shape[0] - h + 1):
            for j in range(board.shape[1] - w + 1):
                cur_board = np.copy(board)
                overlap = False
                for x in range(h):
                    if overlap:
                        break
                    for y in range(w):
                        if p[x][y] != 0 and cur_board[i+x][j+y] == 1:
                            overlap = True
                            break
                        cur_board[i+x][j+y] = p[x][y]
                if not overlap:
                    board_list.append(cur_board)
                    pent_pos_list.append((p, i, j))
    return board_list, pent_pos_list

def pent_trans_repo(pent):          #generate repository of all the transformations of a 
    trans_repo = []                 #certain pent without duplication
    for flip in range(2):
        p = np.copy(pent)   
        if(flip):
            p = np.flip(p,0)
        for _ in range(4):
            p = np.rot90(p)
            trans_repo.append(p)
    result = []
    for p in trans_repo:
        copy = True
        for r in result:
            if np.array_equal(p, r):
                copy = False
                break
        if copy:
            result.append(p)
    return result

def pent_cover_solver(board_mat):           #The exact cover algorithm
    row_num = board_mat.shape[0]
    row_num_list = list(range(row_num))
    cur_sol = []
    return pent_cover_solver_helper(board_mat, cur_sol, row_num_list)

def pent_cover_solver_helper(cur_board_mat, cur_solution, row_num_list):
    height, width = cur_board_mat.shape
    if not width:
        return cur_solution
    c = cur_board_mat.sum(axis=0).argmin()          #sum of columns
    if cur_board_mat.sum(axis=0)[c] == 0:
        return None                                 #no further solutions
    for r in range(height):                         #go through all possible positions
        if not cur_board_mat[r][c]:
            continue
        row_to_delete = []
        col_to_delete = []
        cur_solution.append(row_num_list[r])
        next_board_mat = cur_board_mat
        for j in range(width):
            if not next_board_mat[r][j]:
                continue
            col_to_delete.append(j)
            for i in range(height):
                if next_board_mat[i][j]:
                    if i not in row_to_delete:
                        row_to_delete.append(i)
        next_board_mat = np.delete(next_board_mat, col_to_delete, axis=1)  #delete the column
        next_board_mat = np.delete(next_board_mat, row_to_delete, axis=0)  #delete the row
        new_index = [i for i in list(range(height)) if (i not in row_to_delete)]
        next_row_num_list = [row_num_list[x] for x in new_index]
        sol_result = pent_cover_solver_helper(next_board_mat, cur_solution, next_row_num_list)
        if sol_result:
            return sol_result
        cur_solution.remove(row_num_list[r])
