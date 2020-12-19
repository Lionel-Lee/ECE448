import numpy as np
import utils
import random
import math
import copy
class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        self.reset()
    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def trans_state(self,state):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        '''
        snake_head_x,snake_head_y,snake_body,food_x,food_y=state
        snake_head_x,snake_head_y,food_x,food_y=math.floor(snake_head_x/40), math.floor(snake_head_y/40),math.floor(food_x/40),math.floor(food_y/40)
        snake_body_temp=[]
        for each in snake_body:
            snake_body_temp.append((math.floor(each[0]/40),math.floor(each[1]/40)))
        Adjoining_wall=[0,0]
        Food_dir=[0,0]
        Adjoining_body=[]
        if snake_head_x ==1:
            Adjoining_wall[0] = 1
        if snake_head_x == 12:
            Adjoining_wall[0] = 2
        if snake_head_y ==1:
            Adjoining_wall[1] = 1
        if snake_head_y == 12:
            Adjoining_wall[1] = 2
        if (snake_head_x-food_x != 0):
            Food_dir[0]= 2 if (food_x - snake_head_x > 0) else 1
        if (snake_head_y-food_y != 0):
            Food_dir[1]= 2 if (food_y - snake_head_y > 0) else 1
        #deal with joining body
        for each in [(0,-1),(0,1),(-1,0),(1,0)]:
            if ((snake_head_x+each[0], snake_head_y+each[1]) in snake_body_temp):
                Adjoining_body.append(1)
            else:
                Adjoining_body.append(0)
        return (Adjoining_wall[0],Adjoining_wall[1],Food_dir[0],Food_dir[1],Adjoining_body[0],Adjoining_body[1],Adjoining_body[2],Adjoining_body[3])
    def update_q(self,s,a,state,dead, points):
        last_state = self.trans_state(s)
        reward = -0.1
        if dead == 1:
            reward = -1
        if points - self.points > 0:
            reward = 1

        current_state = self.trans_state(state)
        max_v= float("-inf")
        for i in range(4):
            Qvalue=self.Q[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][i]
            if ( Qvalue> max_v):
                max_v=Qvalue
        alpha = self.C / (self.C + self.N[last_state[0]][last_state[1]][last_state[2]][last_state[3]][last_state[4]][last_state[5]][last_state[6]][last_state[7]][a])
        Q_val = self.Q[last_state[0]][last_state[1]][last_state[2]][last_state[3]][last_state[4]][last_state[5]][last_state[6]][last_state[7]][a]
        return Q_val + alpha * (reward + self.gamma * max_v - Q_val)

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        # temp_state=copy.deepcopy(state)
        temp = state.copy()
        temp[2] = state[2].copy()
        #check if game over
        #update Q table first
        if self.s != None and self.a != None and self.train:
            last_state=self.trans_state(self.s)
            self.Q[last_state[0]][last_state[1]][last_state[2]][last_state[3]][last_state[4]][last_state[5]][last_state[6]][last_state[7]][self.a]=self.update_q(self.s, self.a, state, dead, points)
            if dead == 1:
                self.reset()
                return
        current_state = self.trans_state(state)
        max_v=float("-inf")
        for i in range(4):
            if (self.N[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][i] < self.Ne):
                if (1>=max_v):
                    max_v=1
                    max_action=i
            else:
                Qvalue=self.Q[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][i]
                if ( Qvalue >= max_v):
                    max_v= Qvalue
                    max_action=i  
        self.N[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][max_action] +=1
        # self.s = copy.deepcopy(temp_state)
        self.s = temp
        self.s[2] = temp[2].copy()
        self.a = max_action
        self.points = points      
        return max_action



        
        # tmp = state.copy()
        # tmp[2] = state[2].copy()

        # curr_state = self.trans_state(state)
        # if dead:
        #     last_move_state = self.trans_state(self.s)
        #     self.Q[last_move_state[0]][last_move_state[1]][last_move_state[2]][last_move_state[3]][last_move_state[4]][last_move_state[5]][last_move_state[6]][last_move_state[7]][self.a] = self.update_q(self.s, self.a, state, dead, points)
        #     self.reset()
        #     return

        # if self.s != None and self.a != None and self._train:
        #     last_move_state = self.trans_state(self.s)
        #     new_q = self.update_q(self.s, self.a, state, dead, points)
        #     self.Q[last_move_state[0]][last_move_state[1]][last_move_state[2]][last_move_state[3]][last_move_state[4]][last_move_state[5]][last_move_state[6]][last_move_state[7]][self.a] = new_q

        # # it should return the last one if there is a tie of argmax
        # # utility = [0, 0, 0, 0]
        # # for i in range(4):
        # #     N_val = self.N[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i]
        # #     Q_val = self.Q[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i]
        # #     if N_val < self.Ne:
        # #         utility[i] = 1
        # #     else:
        # #         utility[i] = Q_val

        # # # action = np.argmax(utility)
        # # max_action = max(utility)
        # # for i in range(len(utility)-1, -1, -1):
        # #     if utility[i] == max_action:
        # #         action = i
        # #         break

        # max_v=float("-inf")
        # # max_action=-1
        # for i in range(4):
        #     if (self.N[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i] < self.Ne):
        #         if (1>=max_v):
        #             max_v=1
        #             max_action=i
        #     else:
        #         if (self.Q[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i] >= max_v):
        #             max_v=self.Q[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i]
        #             max_action=i  
        # self.N[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][max_action] += 1
        
        # # discretized state should be passed
        # # deep copy
        # self.s = tmp
        # self.s[2] = tmp[2].copy()
        # self.a = max_action
        # self.points = points
        # return max_action
