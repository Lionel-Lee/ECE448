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

#import mp1
import queue as Q
from maze import Maze
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
    path_queue = []
    visited = set()
    path_queue.append([maze.getStart()])
    while(path_queue):
        now_path = path_queue.pop(0)
        now_point = now_path[-1]
        now_row, now_col = now_point[0], now_point[1]
        if (now_point in visited):
            continue
        if (maze.isObjective(now_row, now_col)):
            # print(now_path)
            visited.add(now_point)
            shortest_path = now_path
            break 
        for point in maze.getNeighbors(now_row, now_col):
            if (point not in visited):
                path_queue.append(now_path + [point])
                visited.add(now_point)
    return shortest_path, len(visited)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    #improved the DFS algorithm to allow better performance
    output_path = [] 
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
            output_path = path
            break
        for neighbor in maze.getNeighbors(x, y):
            if neighbor not in visited:
                stack.append(path + [neighbor])
    return output_path, len(visited)

def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    # get start point and objectives from maze
    start_point = maze.getStart()
    objectives = maze.getObjectives()
    Que = Q.PriorityQueue()
    Que.put([get_man_dis(start_point, objectives), start_point])
    visited = []
    num_states_explored = 0 
    parent = {} 
    while Que:
        current_point = Que.get()[1]
        visited.append(current_point)
        num_states_explored +=1
        #break condition
        if maze.isObjective(current_point[0],current_point[1]):
            dest = current_point
            break
        neighbors = maze.getNeighbors(current_point[0],current_point[1])
        for each in neighbors:
            if (each not in visited):
                if (maze.isValidMove(each[0],each[1])):
                    parent[each] = current_point
                    #push the neighbor to que
                    Que.put([get_man_dis(each, objectives),each])
    return get_path(dest, start_point, parent), num_states_explored

def get_path(dest,start,parent):
    path=[]
    p=dest
    path.append(p)
    while (path[-1] != start):
        p=parent[p]
        path.append(p)
    path.reverse()
    return path

def get_man_dis(p,objectives):
    min_dis = 999999
    for each in objectives:
        man_dis = abs(p[0] - each[0]) + abs(p[1] - each[1])
        if (man_dis < min_dis):
            min_dis = man_dis
    return min_dis

def h_man_dis(start,end):
    return (abs(start[0] - end[0]) + abs(start[1] - end[1]))


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    # get start point and objectives from maze

    if (1 == len(maze.getObjectives())):
        return astar_single(maze)

    return [],0



def astar_single(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    # get start point and objectives from maze
    start_point = maze.getStart()
    end_point = maze.getObjectives()[0]  # one objective situation 
    closed_list = {}
    open_list = Q.PriorityQueue()

    open_list.put((0+h_man_dis(start_point,end_point),[start_point]))

    while open_list:
        current_path = open_list.get()[1]
        current_point = current_path[-1]
        if (current_point in closed_list):
            continue
        closed_list[current_point] = (len(current_path)-1) + h_man_dis(current_point,end_point)   
        if (current_point == end_point):
            return current_path,len(closed_list)
        for neighbor in maze.getNeighbors(current_point[0],current_point[1]):
            f_neighbor = (len(current_path)-1 + 1) + h_man_dis(neighbor,end_point)
            if (neighbor not in closed_list):
                open_list.put((f_neighbor,current_path+[neighbor]))
            elif (closed_list[neighbor] > f_neighbor):                  # not necessary for manhattan dist 
                closed_list[neighbor] = f_neighbor
                open_list.put((f_neighbor,current_path+[neighbor]))
    return [],0