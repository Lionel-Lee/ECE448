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

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


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

        score = 0
        if self.checkWinner() == 1:
            score = 10000
        elif self.checkWinner() == -1:
            score = -10000
        # compute 500 and 100 counter
        five_counter = 0
        one_counter = 0
        for i in range(9):
            row, col = self.globalIdx(i)
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
            temp1 = [self.board[row,col],self.board[row+1][col+1],self.board[row+2, col+2]]
            if ((temp1.count(curPlayer) == 2) and (temp1.count('_') == 1)):
                five_counter += 1
            elif ((temp1.count(oppPlayer) == 2) and (temp1.count(curPlayer) == 1)):
                one_counter += 1
            temp2 = [self.board[row,col+2],self.board[row+1][col+1],self.board[row+2, col]]
            if ((temp2.count(curPlayer) == 2) and (temp2.count('_') == 1)):
                five_counter += 1
            elif ((temp2.count(oppPlayer) == 2) and (temp2.count(curPlayer) == 1)):
                one_counter += 1

            if isMax:
                score += 500 * five_counter + 100 * one_counter
            else:
                score -= 500 * five_counter + 100 * one_counter

            for i in range(9):
                row, col = self.globalIdx[i]
                for y, x in [(row, col), (row + 2, col), (row, col + 2), (row + 2, col + 2)]:
                    if self.board[y][x] == self.maxPlayer:
                        score += 30
                    elif self.board[y][x] == self.minPlayer:
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
                if (self.board[row][col+j] == self.board[row+1][col+j] == self.board[row+2][col+j] != '_'):
                    win_player = self.board[row][col+j]
            # check diagonal
            if (self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] != '_'):
                win_player = self.board[row][col]
            elif (self.board[row][col+2] == self.board[row+1][col+1] == self.board[row+2][col] != '_'):
                win_player = self.board[row][col]
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
        bestValue=0.0
        return bestValue


    def available_move(self,currBoardIdx):
        x=self.globalIdx[currBoardIdx][0]
        y=self.globalIdx[currBoardIdx][1]
        available=[]
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == '_':
                    available.append((i,j))
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
        bestValue=0.0
        if (depth >= self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner()):
            self.expandedNodes +=1
            return self.evaluatePredifined(isMax)
        if isMax:
            bestValue=-10001
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.maxPlayer
                bestValue=max(bestValue, self.minimax(self,depth+1,(iter[0]*3+iter[1]),not isMax))
                self.board[iter[0]][iter[1]] = '_'
        else:
            bestValue=10001
            for iter in self.available_move(currBoardIdx):
                self.board[iter[0]][iter[1]] = self.minPlayer
                bestValue=min(bestValue, self.minimax(self,depth+1,(iter[0]*3+iter[1]),not isMax))
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
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
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
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
