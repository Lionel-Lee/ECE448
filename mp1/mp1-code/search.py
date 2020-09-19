# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    shortest_path = []
    shortest_path_len = 9999
    stack = []
    visited = set()
    init_path = [maze.getStart()]

    stack.append(init_path)
    while (stack):
        path = stack.pop(-1)
        cur_length = len(path)
        x, y = path[-1][0], path[-1][1]
        if ((x,y) in visited):
            continue
        visited.add((x,y))
        if (maze.isObjective(x,y)):
            if(cur_length < shortest_path_len):
                shortest_path = path
                shortest_path_len = cur_length
            continue
        if (cur_length >= shortest_path_len):
            continue
        for neighbor in maze.getNeighbors(x, y):
            if neighbor not in visited:
                stack.append(path + [neighbor])
    return shortest_path, len(visited)

def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0