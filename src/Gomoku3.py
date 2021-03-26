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

    def get_rule_move(self, color):
        moves = self.rules(color)
        random.shuffle(moves)
        if len(moves) == 0:
            return "draw"
        return moves[0]

    def rules(self, color):
        win = []
        block = []
        open_four = []
        block_open_four = []
        random = []

        for move in self.board.get_empty_points:
            for two_directions in [["N","S"], ["NE","SW"], ["E","W"], ["SE","NW"]]:
                stats = self.line_rule(color, move, two_directions)
                if stats["win"]:
                    win.append(move)
                elif stats["block"]:
                    block.append(move)
                elif stats["open_four"]:
                    block.append(move)
                elif stats["block_open_four"]:
                    block_open_four.append(move)
                else:
                    random.append(move)

        if len(win) > 0:
            return win
        if len(block) > 0:
            return block
        if len(open_four) > 0:
            return open_four
        if len(block_open_four):
            return block_open_four
        if len(random) > 0:
            return random
        return "pass"

    def line_rule(self, color, pos, two_directions):
        l_mine = 0
        l_theirs = 0
        l_open = 0
        r_mine = 0
        r_theirs = 0
        r_open = 0

        increment = self.board.increments[two_directions[0]]
        next_pos = pos+increment
        pos_color = self.board.get_color(next_pos)
        while (pos_color!=BORDER and l_open<=1):
            if pos_color == color:
                l_mine += 1
                if l_theirs >= 1:
                    break
            elif pos_color == EMPTY:
                l_open += 1
                break
            else:
                l_theirs += 1
                if l_mine >= 1:
                    break

        increment = self.board.increments[two_directions[1]]
        next_pos = pos+increment
        pos_color = self.board.get_color(next_pos)
        while (pos_color!=BORDER and r_open<=1):
            if pos_color == color:
                r_mine += 1
                if r_theirs >= 1:
                    break
            elif pos_color == EMPTY:
                r_open += 1
                if r_mine+l_theirs >= 1:
                    break
            else:
                r_theirs += 1
                if r_mine >= 1:
                    break

        stats = {"win":False, "block_win":False, "open_four":False, "block_open_four":False}

        if l_mine + r_mine >= 4:
            stats["win"] = True
            return stats
        if l_theirs + r_theirs >= 4:
            stats["block_win"] = True
            return stats
        if l_mine + r_mine == 3 and l_open + r_open == 2:
            stats["open_four"] = True
            return stats
        if l_theirs + r_theirs == 3 and l_open + r_open == 2:
            stats["block_open_four"] = True
            return stats

        return stats
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    player=FlatMCSimPlayer(10,board)
    player.startSimulation('b')

if __name__ == "__main__":
    run()