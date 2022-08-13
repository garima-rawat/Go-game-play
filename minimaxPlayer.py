import sys
from read import readInput
from write import writeOutput
from copy import deepcopy

from host import GO


class TreeNode():
    def __init__(self, currentState: GO, i :int, j:int, childStates = [] ):
        self.currentState = currentState
        self.i = i
        self.j = j
        self.childStates = childStates
    


    def terminalHeuristics(self, piece_type):
        '''
        Calculates heuristics(actual game end score for terminal state)
        '''
        value = 0
        currBoard = self.currentState.board
        for i in range(5):
            for j in range(5):

                if currBoard[i][j]==piece_type:
                    value += 1
                if currBoard[i][j]==3-piece_type:
                    value -= 1
        #print("heuristic ", value)
        return value

    def broadHeuristics(self, piece_type):
        value = 0
        currBoard = self.currentState.board
        for i in range(5):
            for j in range(5):

                if currBoard[i][j]==piece_type:
                    value += 1

                    if i-1>=0 and currBoard[i-1][j] == 0:
                        value += 0.5

                    if i+1<5 and currBoard[i+1][j] == 0:
                        value += 0.5

                    if j-1>=0 and currBoard[i][j-1] == 0:
                        value += 0.5

                    if j+1<0 and currBoard[i][j+1] == 0:
                        value += 0.5

                    if i-1>=0 and currBoard[i-1][j] == 3-piece_type:
                        value -= 0.75

                    if i+1<5 and currBoard[i+1][j] == 3-piece_type:
                        value -= 0.75

                    if j-1>=0 and currBoard[i][j-1] == 3-piece_type:
                        value -= 0.75

                    if j+1<5 and currBoard[i][j+1] == 3-piece_type:
                        value -= 0.75

                if currBoard[i][j]==3-piece_type:
                    value -= 1.5

                    if i-1>=0 and currBoard[i-1][j] == 0:
                        value -= 0.5

                    if i+1<5 and currBoard[i+1][j] == 0:
                        value -= 0.5

                    if j-1>=0 and currBoard[i][j-1] == 0:
                        value -= 0.5

                    if j+1<5 and currBoard[i][j+1] == 0:
                        value -= 0.5

                    if i-1>=0 and currBoard[i-1][j]==piece_type:
                        value += 0.75

                    if i+1<5 and currBoard[i+1][j]==piece_type:
                        value += 0.75

                    if j-1>=0 and currBoard[i][j-1]==piece_type:
                        value += 0.75

                    if j+1<5 and currBoard[i][j+1]==piece_type:
                        value += 0.75

                
        #print("heuristic ", value)
        return value

    def heuristics(self, piece_type):
        '''
        Heuristic function for non terminating states
        '''
        value = 0
        currBoard = self.currentState.board
        visited = set()

        def detect_neighbor(i, j):
            neighbors = []
            # Detect borders and add neighbor coordinates
            if i > 0: neighbors.append((i-1, j))
            if i < len(currBoard) - 1: neighbors.append((i+1, j))
            if j > 0: neighbors.append((i, j-1))
            if j < len(currBoard) - 1: neighbors.append((i, j+1))
            return neighbors

        def detect_neighbor_ally(i, j):
            '''
            Detect the neighbor allies of a given stone.

            :param i: row number of the board.
            :param j: column number of the board.
            :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
            '''
            
            neighbors = detect_neighbor(i, j)  # Detect neighbors
            group_allies = []
            # Iterate through neighbors
            for piece in neighbors:
                # Add to allies list if having the same color
                if board[piece[0]][piece[1]] == currBoard[i][j]:
                    group_allies.append(piece)
            return group_allies

        def ally_dfs(i, j):
            '''
            Using DFS to search for all allies of a given stone.

            :param i: row number of the board.
            :param j: column number of the board.
            :return: a list containing the all allies row and column (row, column) of position (i, j).
            '''
            stack = [(i, j)]  # stack for DFS serach
            ally_members = []  # record allies positions during the search
            while stack:
                piece = stack.pop()
                ally_members.append(piece)
                neighbor_allies = detect_neighbor_ally(piece[0], piece[1])
                for ally in neighbor_allies:
                    if ally not in stack and ally not in ally_members:
                        stack.append(ally)
            return ally_members

        def find_liberty(i, j):
            '''
            Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

            :param i: row number of the board.
            :param j: column number of the board.
            :return: boolean indicating whether the given stone still has liberty.
            '''

            cnt = 0
            ally_members = ally_dfs(i, j)
            for member in ally_members:
                visited.add((member[0], member[1])) ##mine
                neighbors = detect_neighbor(member[0], member[1])
                for piece in neighbors:
                    # If there is empty space around a piece, it has liberty
                    if currBoard[piece[0]][piece[1]] == 0:
                        cnt +=1 
            return cnt
            # If none of the pieces in a allied group has an empty space, it has no liberty
            

        for i in range(5):
            for j in range(5):
                
                if currBoard[i][j] == piece_type:
                    value += 4
                elif currBoard[i][j] == 3-piece_type:
                    value -= 5

                if (i,j) in visited or currBoard[i][j]==0:
                    continue
                visited.add((i,j))
                
                if currBoard[i][j] == piece_type:
                    value += find_liberty(i, j)
                else:
                    value -= find_liberty(i, j)
        
        return value



class MyPlayer():
    def __init__(self, piece_type: int):
        self.type = 'MyPlayer'
        self.piece_type = piece_type
        self.searchDepth = 3
        self.terminal = 1

    def writeIteration(self, iter_count: int):
        f = open("iteration_count.txt", "w")
        f.write(str(iter_count))
        f.close()

    def readIteration(self, go: GO):

        if go.previous_board==go.board: ## new game
            self.iter_count = 1
        elif previous_board == [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]:
            self.iter_count = 2
        else:
            with open('iteration_count.txt') as f:
                lines = f.readlines()
            f.close()
            self.iter_count = int(lines[0])+2

        self.writeIteration(self.iter_count)


    def get_input(self, go: GO):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        self.readIteration(go)

        ## initial moves
        if self.iter_count<=17:
            self.searchDepth = 3
            self.terminal = 1


        elif 18<=self.iter_count<=20:
            self.searchDepth = 4
            self.terminal = 1

        ## final moves
        else: ## self.iter_count>=21:
            self.searchDepth = 25-self.iter_count
            self.terminal = 3



        print("iteration", self.iter_count)
        self.root = TreeNode(go, 0, 0, [])
        self.setTree(self.root, self.piece_type, 0)


        _, move_i, move_j = self.minimax(self.root, 0)
        return (move_i, move_j)


    def setTree(self, root: TreeNode, piece_type: int, level:int):
        '''
        Sets the state search tree for minimax algortihm till searchDepth levels
        each node of the tree is of type TreeNode and represents the state of the game at that level and move

        '''

        if level == self.searchDepth:
            return
                
        currState = root.currentState
        
        for i in range(5):
            for j in range(5):
                
                if currState.board[i][j]!=0:
                    continue
                newState = currState.copy_board()
                valid = newState.place_chess(i, j, piece_type)
                
                if not valid:
                    continue
                newState.remove_died_pieces(3-piece_type)

                alpha = TreeNode(newState, i, j, [])
                root.childStates.append(alpha)
                
                self.setTree(alpha, 3-piece_type, level+1)

        ## for PASS
        newState = currState.copy_board()
        alpha = TreeNode(newState, 5, 5, [])
        root.childStates.append(alpha)
        self.setTree(alpha, 3-piece_type, level+1)
        
        return


    def minimax(self, root: TreeNode, level: int):
        '''

        param root: the root of states Tree at which we calculate min/max
        param level: the level to indicate whether we are calculating min or max
        
        Calculates Min max values and returns the final move to original function
        '''

        ## leaf nodes require heuristic calculation of their state
        if root.childStates == []:
            if self.terminal==1:
                value = root.heuristics(self.piece_type)
            elif self.terminal==2:
                value = root.broadHeuristics(self.piece_type)
            else:
                value = root.terminalHeuristics(self.piece_type)
            return value, -1, -1

        ## Max levels
        if level%2 == 0:
            final_max = -1000000
            
            for child in root.childStates:
                value, _, _ = self.minimax(child, level+1)
                if value > final_max:
                    final_max = value
                    final_i = child.i
                    final_j = child.j
            return final_max, final_i, final_j

        ## Min levels
        elif level%2 == 1:
            final_min = 1000000
            for child in root.childStates:
                value, _, _ = self.minimax(child, level+1)
                if value < final_min:
                    final_min = value
                    
            return final_min, -1, -1


    

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)

    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MyPlayer(piece_type)
    action = player.get_input(go)
    if action == (5,5):
        action = "PASS"
    #print("action", action)
    writeOutput(action)