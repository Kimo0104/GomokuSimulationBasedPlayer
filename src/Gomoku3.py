from gtp_connection import GtpConnection
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    MAXSIZE,
    coord_to_point,
    WIN_CONDITION
)
from board import GoBoard
import copy
import random
class FlatMCSimPlayer:
    def __init__(self,numSimulations,board):
        self.numSimulations=numSimulations
        self.board=board


    def startSimulation(self,board_color):
        color = self.color_to_int(board_color)
        legalMoves = GoBoardUtil.generate_legal_moves(self.board,color)
        numLegalMoves=len(legalMoves)
        scores = [0] * numLegalMoves
        for i in range (len(legalMoves)):
            move = legalMoves[i]
            scores[i] = self.simulate(move,color)
            break

    def simulate(self,move,color):
        stats = {'b':0 , 'w':0, 'd':0}
        movesMade=[]
        #Append move which will start the simulation

        self.board.play_move(move,color)
        color=GoBoardUtil.opponent(color)
        movesMade.append(move)
        for i in range(self.numSimulations):
            while self.board.get_result(color,move,5)=='unknown':
                move=GoBoardUtil.generate_random_move(self.board,color)
                self.board.play_move(move,color)
                color=GoBoardUtil.opponent(color)
                movesMade.append(move)
            print(self.board.get_result(color,move,5))
        self.board2d()

        for moveMade in movesMade:
            self.board.undo_move(moveMade)

    def color_to_int(self,c):
        """convert character to the appropriate integer code"""
        color_to_int = {"b": BLACK, "w": WHITE, "e": EMPTY, "BORDER": BORDER}
        return color_to_int[c]

    def board2d(self):
        print(str(GoBoardUtil.get_twoD_board(self.board)))
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    player=FlatMCSimPlayer(10,board)
    player.startSimulation('b')

if __name__ == "__main__":
    run()