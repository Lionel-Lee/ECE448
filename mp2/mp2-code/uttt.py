from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

        self.A = 0.5
        self.B = 1 - self.A 

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        # print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

        for x1 in range(3):
            for x2 in range(3):
                print(' '.join(str(a) for a in self.board[x1*3+x2][0:3]) + ' | ' + \
                        ' '.join(str(a) for a in self.board[x1*3+x2][3:6]) + ' | ' +\
                        ' '.join(str(a) for a in self.board[x1*3+x2][6:9]))
            print('\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE

        if (isMax and self.checkWinner() == 1):
            return 10000
        elif (not isMax and self.checkWinner() == -1):
            return -10000

        # compute 500 and 100 counter
        score = 0
        five_counter = 0
        one_counter = 0
        for i in range(9):
            row, col = self.globalIdx[i]
            if (isMax):
                curPlayer = self.maxPlayer
                oppPlayer = self.minPlayer
            else:
                curPlayer = self.minPlayer
                oppPlayer = self.maxPlayer
            # check row
            for j in range(3):
                temp = []
                for k in range(3):
                    temp.append(self.board[row+j][col+k])
                if ((temp.count(curPlayer) == 2) and (temp.count('_') == 1)):
                    five_counter += 1
                elif((temp.count(oppPlayer) == 2) and (temp.count(curPlayer) == 1)):
                    one_counter += 1
            # check col
            for j in range(3):
                temp = []
                for k in range(3):
                    temp.append(self.board[row+k][col+j])
                if ((temp.count(curPlayer) == 2) and (temp.count('_') == 1)):
                    five_counter += 1
                elif((temp.count(oppPlayer) == 2) and (temp.count(curPlayer) == 1)):
                    one_counter += 1
            # check diagonal
            temp1 = [self.board[row][col],self.board[row+1][col+1],self.board[row+2][col+2]]
            if ((temp1.count(curPlayer) == 2) and (temp1.count('_') == 1)):
                five_counter += 1
            elif ((temp1.count(oppPlayer) == 2) and (temp1.count(curPlayer) == 1)):
                one_counter += 1
            temp2 = [self.board[row][col+2],self.board[row+1][col+1],self.board[row+2][col]]
            if ((temp2.count(curPlayer) == 2) and (temp2.count('_') == 1)):
                five_counter += 1
            elif ((temp2.count(oppPlayer) == 2) and (temp2.count(curPlayer) == 1)):
                one_counter += 1

        if isMax:
            score += 500 * five_counter + 100 * one_counter
        else:
            score -= (100 * five_counter + 500 * one_counter)

        #rule 3
        if 0 == score:
            for i in range(9):
                row, col = self.globalIdx[i]
                for y, x in [(row, col), (row + 2, col), (row, col + 2), (row + 2, col + 2)]:
                    if self.board[y][x] == self.maxPlayer and isMax:
                        score += 30
                    elif self.board[y][x] == self.minPlayer and not isMax:
                        score -= 30

        return score
    
    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        if (isMax and self.checkWinner() == 1):
            return 10000
        elif (not isMax and self.checkWinner() == -1):
            return -10000

        # compute 500 and 100 counter
        score = 0
        five_counter = 0
        one_counter = 0
        for i in range(9):
            row, col = self.globalIdx[i]
            if (isMax):
                curPlayer = self.maxPlayer
                oppPlayer = self.minPlayer
            else:
                curPlayer = self.minPlayer
                oppPlayer = self.maxPlayer
            # check row
            for j in range(3):
                temp = []
                for k in range(3):
                    temp.append(self.board[row+j][col+k])
                if ((temp.count(curPlayer) == 2) and (temp.count('_') == 1)):
                    five_counter += 1
                elif((temp.count(oppPlayer) == 2) and (temp.count(curPlayer) == 1)):
                    one_counter += 1
            # check col
            for j in range(3):
                temp = []
                for k in range(3):
                    temp.append(self.board[row+k][col+j])
                if ((temp.count(curPlayer) == 2) and (temp.count('_') == 1)):
                    five_counter += 1
                elif((temp.count(oppPlayer) == 2) and (temp.count(curPlayer) == 1)):
                    one_counter += 1
            # check diagonal
            temp1 = [self.board[row][col],self.board[row+1][col+1],self.board[row+2][col+2]]
            if ((temp1.count(curPlayer) == 2) and (temp1.count('_') == 1)):
                five_counter += 1
            elif ((temp1.count(oppPlayer) == 2) and (temp1.count(curPlayer) == 1)):
                one_counter += 1
            temp2 = [self.board[row][col+2],self.board[row+1][col+1],self.board[row+2][col]]
            if ((temp2.count(curPlayer) == 2) and (temp2.count('_') == 1)):
                five_counter += 1
            elif ((temp2.count(oppPlayer) == 2) and (temp2.count(curPlayer) == 1)):
                one_counter += 1

        if isMax:
            score += 500 * five_counter + 100 * one_counter
        else:
            score -= 200 * five_counter + 400 * one_counter

        #rule 3
        # if 0 == score:
        for i in range(9):
            row, col = self.globalIdx[i]
            for y, x in [(row, col), (row + 2, col), (row, col + 2), (row + 2, col + 2)]:
                if self.board[y][x] == self.maxPlayer and isMax:
                    score += 30
                elif self.board[y][x] == self.minPlayer and not isMax:
                    score -= 30

        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        movesLeft = False
        for sublist in self.board:
            for element in sublist:
                if (element == '_'):
                    movesLeft = True
        return movesLeft

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        winner = 0
        win_player = ''
        
        for i in range(9):
            row, col = self.globalIdx[i]
            # check row
            for j in range(3):
                if (self.board[row+j][col] == self.board[row+j][col+1] == self.board[row+j][col+2] != '_'):

                    win_player = self.board[row+j][col]
            # check columun
            for k in range(3):
                if (self.board[row][col+k] == self.board[row+1][col+k] == self.board[row+2][col+k] != '_'):
  
                    win_player = self.board[row][col+k]
            # check diagonal
            if (self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] and self.board[row][col] != '_'):
      
                win_player = self.board[row][col]
            elif (self.board[row][col+2] == self.board[row+1][col+1] == self.board[row+2][col] and self.board[row][col+2] != '_'):

                win_player = self.board[row][col+2]

        if(win_player == self.maxPlayer):
            winner = 1
        elif(win_player == self.minPlayer):
            winner = -1
        return winner

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        self.expandedNodes += 1
        
        if (depth >= self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            return self.evaluatePredifined(not isMax)

        if isMax:
            bestValue = -inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.maxPlayer
                bestValue = max(bestValue, self.alphabeta(depth+1, ((iter[0]%3)*3 + iter[1]%3), alpha,beta,not isMax))
                self.board[iter[0]][iter[1]] = '_'
                if bestValue >= beta:
                    return bestValue
                alpha=max(bestValue,alpha)
                # print(alpha,' ',beta)

        else:
            bestValue = inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.minPlayer
                bestValue = min(bestValue, self.alphabeta(depth+1, ((iter[0]%3)*3+iter[1]%3), alpha,beta,not isMax))
                self.board[iter[0]][iter[1]] = '_'
                if bestValue <= alpha:
                    return bestValue
                beta=min(beta,bestValue)


        return bestValue

    def new_alpha_beta(self,depth,currBoardIdx,alpha,beta,isMax):
        self.expandedNodes += 1
        
        if (depth >= self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            return self.evaluateDesigned(not isMax)

        if isMax:
            bestValue = -inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.maxPlayer
                bestValue = max(bestValue, self.A * self.new_alpha_beta(depth+1, ((iter[0]%3)*3 + iter[1]%3), alpha,beta,not isMax) + \
                                    self.B * self.evaluateDesigned(not isMax))
                self.board[iter[0]][iter[1]] = '_'
                if bestValue >= beta:
                    return bestValue
                alpha=max(bestValue,alpha)
                # print(alpha,' ',beta)

        else:
            bestValue = inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.minPlayer
                bestValue = min(bestValue, self.A * self.new_alpha_beta(depth+1, ((iter[0]%3)*3+iter[1]%3), alpha,beta,not isMax) + \
                                            self.B * self.evaluateDesigned(not isMax))
                self.board[iter[0]][iter[1]] = '_'
                if bestValue <= alpha:
                    return bestValue
                beta=min(beta,bestValue)


        return bestValue


    def available_move(self,currBoardIdx):

        x, y = self.globalIdx[currBoardIdx]

        available=[]
        for i in range(3):
            for j in range(3):
                if self.board[x+i][y+j] == '_':
                    available.append((x+i,y+j))
        return available

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        self.expandedNodes += 1
        if (depth >= self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            return self.evaluatePredifined(not isMax)

        if isMax:
            bestValue = -inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.maxPlayer
                bestValue = max(bestValue, self.minimax(depth+1, ((iter[0]%3)*3 + iter[1]%3), not isMax))
                self.board[iter[0]][iter[1]] = '_'
        else:
            bestValue = inf
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.minPlayer
                bestValue = min(bestValue, self.minimax(depth+1, ((iter[0]%3)*3+iter[1]%3), not isMax))
                self.board[iter[0]][iter[1]] = '_'
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        gameBoards = []
        expandedNodes = []
        bestMove = []
        bestValue = []
        self.currPlayer = maxFirst           # True for max, False for min
        cur_board_idx = self.startBoardIdx
        alpha = -inf
        beta = inf

        while((self.checkWinner() == 0) and self.checkMovesLeft()):

            x, y = self.globalIdx[cur_board_idx]
            if self.currPlayer:
                player = self.maxPlayer
                best_value = -inf
            else:
                player = self.minPlayer
                best_value = inf

            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        self.board[x+i][y+j] = player       #one valid move
                        
                        next_board_idx = ((x+i) % 3) * 3 + (y+j) % 3
                        if (self.currPlayer and isMinimaxOffensive) or \
                            (not self.currPlayer and isMinimaxDefensive):
                            attempt_value = self.minimax(0, next_board_idx, not self.currPlayer)
                        else:
                            attempt_value = self.alphabeta(0, next_board_idx, alpha, beta, not self.currPlayer)
                            # if self.currPlayer:
                            #     alpha=max(alpha,attempt_value)
                            # if not self.currPlayer:
                            #     beta=min(beta,attempt_value)
                        
                        self.board[x+i][y+j] = '_'          #remove the attempt move

                        if (self.currPlayer and attempt_value > best_value) or \
                            (not self.currPlayer and attempt_value < best_value):
                            best_value = attempt_value
                            best_move = (x+i, y+j)

            self.board[best_move[0]][best_move[1]] = player #deciede the move

            cur_board_idx = (best_move[0]%3) * 3 + best_move[1]%3       #update board idx
            expandedNodes.append(self.expandedNodes)
            gameBoards.append(self.board)
            bestMove.append(best_move)
            bestValue.append(best_value)
            self.currPlayer = not self.currPlayer           #swap player

            self.printGameBoard()
            print('=======================')
     
        self.printGameBoard()
        winner = self.checkWinner()
  
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameYourAgent(self,maxFirst):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
   
        gameBoards = []
        expandedNodes = []
        bestMove = []
        bestValue = []
        self.currPlayer = maxFirst           # True for max, False for min
        cur_board_idx = self.startBoardIdx
        alpha = -inf
        beta = inf
        while((self.checkWinner() == 0) and self.checkMovesLeft()):
            x, y = self.globalIdx[cur_board_idx]
            if self.currPlayer:
                player = self.maxPlayer
                best_value = -inf
            else:
                player = self.minPlayer
                best_value = inf

            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        self.board[x+i][y+j] = player       #one valid move
                        
                        next_board_idx = ((x+i) % 3) * 3 + (y+j) % 3
                        if self.currPlayer:
                            attempt_value=self.alphabeta(0, next_board_idx, alpha, beta, not self.currPlayer)
                        if not self.currPlayer:
                            attempt_value=self.A * self.new_alpha_beta(0, next_board_idx, alpha, beta, not self.currPlayer) + \
                                           self.B * self.evaluateDesigned(not self.currPlayer)
                        
                        self.board[x+i][y+j] = '_'          #remove the attempt move

                        if (self.currPlayer and attempt_value > best_value) or \
                            (not self.currPlayer and attempt_value < best_value):
                            best_value = attempt_value
                            best_move = (x+i, y+j)

            self.board[best_move[0]][best_move[1]] = player #deciede the move

            cur_board_idx = (best_move[0]%3) * 3 + best_move[1]%3       #update board idx
            expandedNodes.append(self.expandedNodes)
            gameBoards.append(self.board)
            bestMove.append(best_move)
            bestValue.append(best_value)
            self.currPlayer = not self.currPlayer           #swap player

            # self.printGameBoard()
            # print('=======================')

        winner = self.checkWinner()
        return gameBoards, bestMove, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        #YOUR CODE HERE
        gameBoards = []
        expandedNodes = []
        bestMove = []
        bestValue = []
        maxFirst=True
        self.currPlayer = maxFirst           # True for max, False for min
        cur_board_idx = self.startBoardIdx
        alpha = -inf
        beta = inf

        while((self.checkWinner() == 0) and self.checkMovesLeft()):

            x, y = self.globalIdx[cur_board_idx]
            if self.currPlayer:
                player = self.maxPlayer
                best_value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            self.board[x+i][y+j] = player       #one valid move
                            next_board_idx = ((x+i) % 3) * 3 + (y+j) % 3
                            attempt_value = self.alphabeta(0, next_board_idx, alpha, beta, not self.currPlayer)
                            self.board[x+i][y+j] = '_'          #remove the attempt move
                            if (attempt_value > best_value):
                                best_value = attempt_value
                                best_move = (x+i, y+j)
                self.board[best_move[0]][best_move[1]] = self.maxPlayer #deciede the move
            else:
                print("Determine your decision!")
                x = int(input("Row position: "))
                y = int(input("Column position: "))
                while not checkvalid(self,x,y,cur_board_idx) :
                    print("This position is not valid, try again!")
                    x = int(input("Row position: "))
                    y = int(input("Column position: "))
                best_move=(x,y)
                self.board[best_move[0]][best_move[1]] = self.minPlayer #deciede the move

            cur_board_idx = (best_move[0]%3) * 3 + best_move[1]%3       #update board idx
            expandedNodes.append(self.expandedNodes)
            gameBoards.append(self.board)
            bestMove.append(best_move)
            bestValue.append(best_value)
            self.currPlayer = not self.currPlayer           #swap player

            self.printGameBoard()
            print('=======================')

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

def checkvalid(self,x,y,currBoardIdx):
    print(self.globalIdx[currBoardIdx][0]," ",self.globalIdx[currBoardIdx][1])
    if (x<0 or x>8 or y<0 or y>8):
        return False
    if (self.board[x][y] != '_'):
        return False
    if (x<self.globalIdx[currBoardIdx][0] or x>self.globalIdx[currBoardIdx][0]+2 or y<self.globalIdx[currBoardIdx][1] or y>self.globalIdx[currBoardIdx][1]+2):
        return False
    return True
    
if __name__=="__main__":
    uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGameHuman()
    # win=0
    # lose=0
    # whether =0
    # for i in range(18):
    #     uttt=ultimateTicTacToe()
    #     winner=0
    #     # whether=randint(0,1)
    #     uttt.startBoardIdx=int(i/2)
    #     gameBoards, bestMove, winner = uttt.playGameYourAgent(whether)
    #     whether = 1- whether
    #     uttt.printGameBoard()
    #     # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    #     if winner == 1:
    #         print("The winner is maxPlayer!!!")
    #         win+=1
    #     elif winner == -1:
    #         print("The winner is minPlayer!!!")
    #         lose+=1
    #     else:
    #         print("Tie. No winner:(")
    #     continue

    # print(win,lose)

    # uttt.printGameBoard()
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")
