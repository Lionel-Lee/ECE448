# -*- coding: utf-8 -*-
import numpy as np

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """

    board = 1 - board           #swap 0 and 1, 0 for available place
    # result_list = []
    # # result_list = solve_helper(cur_board, pents, 0, result_list)[0]
    # return result_list
    flat_board = board.ravel()
    list_to_delete = np.where(flat_board == 1)
    list_to_delete = [x + len(pents) for x in list_to_delete]

    matrix = []
    info_matrix = []
    for i in range(len(pents)):
        all_pos_list, all_pos_info = pent_possible_place(board, pents[i])
        for item in all_pos_list:
            item = np.append(np.zeros(len(pents)), item)
            item = np.delete(item, list_to_delete)
            item[i] = 1
            matrix.append(item)
        info_matrix.extend(all_pos_info)

    # matrix is the big 2000 * 72 for exact cover algorithm X
    matrix = np.array(matrix)
    # print("matrix row numbers:", len(matrix))

    matrix[matrix > 0] = 1
    result_list = exact_cover(matrix)

    return_val = []
    for i in result_list:
        info = info_matrix[i]
        # print(info)
        return_val.append((info[0], (info[1], info[2])))
    return return_val

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
#     """
#     Adds a pentomino pent to the board. The pentomino will be placed such that
#     coord[0] is the lowest row index of the pent and coord[1] is the lowest 
#     column index. 
    
#     check_pent will also check if the pentomino is part of the valid pentominos.
#     """
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

def exact_cover(matrix):
    return exact_cover_helper(matrix, [], list(range(matrix.shape[0])))

def exact_cover_helper(A, partial, original_r):
    row, col = A.shape
    if col == 0:
        return partial
    else:
        c = A.sum(axis=0).argmin()
        if A.sum(axis=0)[c] == 0:
            return None
        partial_temp = partial
        for r in range(row):
            B = A
            if B[r][c] != 1:
                continue
            r_index = original_r[r]
            partial_temp.append(r_index)
            col_temp = []
            row_temp = []
            for j in range(col):
                if B[r][j] != 1:
                    continue
                col_temp.append(j)
                for i in range(row):
                    if B[i][j] == 1:
                        if i not in row_temp:
                            row_temp.append(i)
            # Delete each row i such that A[i,j] = 1
            # then delete column j.
            B = np.delete(B, row_temp, axis=0)
            B = np.delete(B, col_temp, axis=1)
            new_index = [x for x in list(range(row)) if x not in row_temp]
            new_r = [original_r[x] for x in new_index]
            answer = exact_cover_helper(B, partial_temp, new_r)
            if answer != None:
                return answer
            partial_temp.remove(r_index)
