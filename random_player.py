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


    def heuristics(self, piece_type):
        value = 0
        currBoard = self.currentState.board
        for i in range(5):
            for j in range(5):

                if currBoard[i][j]==piece_type:
                    value += 1

                    if i-1>=0 and currBoard[i-1][j]==0:
                        value += 0.5

                    if i+1<5 and currBoard[i+1][j]==0:
                        value += 0.5

                    if j-1>=0 and currBoard[i][j-1]==0:
                        value += 0.5

                    if j+1<0 and currBoard[i][j+1]==0:
                        value += 0.5

                    if i-1>=0 and currBoard[i-1][j]==3-piece_type:
                        value -= 0.75

                    if i+1<5 and currBoard[i+1][j]==3-piece_type:
                        value -= 0.75

                    if j-1>=0 and currBoard[i][j-1]==3-piece_type:
                        value -= 0.75

                    if j+1<5 and currBoard[i][j+1]==3-piece_type:
                        value -= 0.75

                if currBoard[i][j]==3-piece_type:
                    value -= 1.5

                    if i-1>=0 and currBoard[i-1][j]==0:
                        value -= 0.5

                    if i+1<5 and currBoard[i+1][j]==0:
                        value -= 0.5

                    if j-1>=0 and currBoard[i][j-1]==0:
                        value -= 0.5

                    if j+1<5 and currBoard[i][j+1]==0:
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



class RandomPlayer():
    def __init__(self, piece_type: int):
        self.type = 'random'
        self.piece_type = piece_type
        self.terminal = False



    def get_input(self, go: GO, piece_type: int):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        

        self.searchDepth = 3

        self.root = TreeNode(go, 0, 0, [])
        self.setTree(self.root, piece_type, 0)


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
            value = root.terminalHeuristics(self.piece_type) if self.terminal else root.heuristics(self.piece_type)
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
    player = RandomPlayer(piece_type)
    action = player.get_input(go, piece_type)
    if action == (5,5):
        action = "PASS"
    print(action)
    writeOutput(action)