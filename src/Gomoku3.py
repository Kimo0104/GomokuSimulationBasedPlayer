from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard

class FlatMonteCarloSimulationPlayer:
    def __init__(self,numSimulations,board):
        self.numSimulations=numSimulations
        self.board=board
        self.gtpConnection = GtpConnection(board)

    def genmove(self,board,board_color):
        color = color_to_int(board_color)
        legalMoves = GoBoardUtil.generate_legal_moves(board,color)
        
    
def color_to_int(c):
    """convert character to the appropriate integer code"""
    color_to_int = {"b": GoBoardUtil.BLACK, "w": GoBoardUtil.WHITE, "e": GoBoardUtil.EMPTY, "BORDER": GoBoardUtil.BORDER}
    
    try:
        return color_to_int[c]
    except:
        raise KeyError("\"{}\" wrong color".format(c))
    
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    player=FlatMonteCarloSimulationPlayer(10,board)

if __name__ == "__main__":
    pass