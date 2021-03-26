"""
board.py

Implements a basic Go board with functions to:
- initialize to a given board size
- check if a move is legal
- play a move

The board uses a 1-dimensional representation with padding
"""

import numpy as np
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    is_black_white,
    is_black_white_empty,
    coord_to_point,
    where1d,
    MAXSIZE,
    GO_POINT
)

"""
The GoBoard class implements a board and basic functions to play
moves, check the end of the game, and count the score at the end.
The class also contains basic utility functions for writing a Go player.
For many more utility functions, see the GoBoardUtil class in board_util.py.

The board is stored as a one-dimensional array of GO_POINT in self.board.
See GoBoardUtil.coord_to_point for explanations of the array encoding.
"""
class GoBoard(object):
    def __init__(self, size):
        """
        Creates a Go board of given size
        """
        assert 2 <= size <= MAXSIZE
        self.reset(size)
        self.increments = {"N":-self.size-1, "NW":-self.size-2, "W":-1, "SW":self.size, 
                           "S":self.size+1, "SE":self.size+2, "E":1, "NE":-self.size}

    def reset(self, size):
        """
        Creates a start state, an empty board with given size.
        """
        self.size = size
        self.NS = size + 1
        self.WE = 1
        self.last_move = None
        self.last2_move = None
        self.current_player = BLACK
        self.maxpoint = size * size + 3 * (size + 1)
        self.board = np.full(self.maxpoint, BORDER, dtype=GO_POINT)
        self._initialize_empty_points(self.board)
        self.increments = {"N":-self.size-1, "NW":-self.size-2, "W":-1, "SW":self.size, 
                           "S":self.size+1, "SE":self.size+2, "E":1, "NE":-self.size}

    def copy(self):
        b = GoBoard(self.size)
        assert b.NS == self.NS
        assert b.WE == self.WE
        b.last_move = self.last_move
        b.last2_move = self.last2_move
        b.current_player = self.current_player
        b.board = np.copy(self.board)
        return b

    def get_color(self, point):
        return self.board[point]

    def pt(self, row, col):
        return coord_to_point(row, col, self.size)

    def coord(self, pt):
        pt = pt - ((pt-1)//(self.size+1)) - (self.size+1)

        return chr(ord("A")+(pt%self.size))+str((pt//self.size)+1)

    def is_legal(self, point, color):
        """
        Check whether it is legal for color to play on point
        This method tries to play the move on a temporary copy of the board.
        This prevents the board from being modified by the move
        """
        board_copy = self.copy()
        can_play_move = board_copy.play_move(point, color)
        return can_play_move

    def get_empty_points(self):
        """
        Return:
            The empty points on the board
        """
        return where1d(self.board == EMPTY)

    def row_start(self, row):
        assert row >= 1
        assert row <= self.size
        return row * self.NS + 1

    def _initialize_empty_points(self, board):
        """
        Fills points on the board with EMPTY
        Argument
        ---------
        board: numpy array, filled with BORDER
        """
        for row in range(1, self.size + 1):
            start = self.row_start(row)
            board[start : start + self.size] = EMPTY

    def get_size(self):
        return self.size

    # def is_eye(self, point, color):
    #     """
    #     Check if point is a simple eye for color
    #     """
    #     if not self._is_surrounded(point, color):
    #         return False
    #     # Eye-like shape. Check diagonals to detect false eye
    #     opp_color = GoBoardUtil.opponent(color)
    #     false_count = 0
    #     at_edge = 0
    #     for d in self._diag_neighbors(point):
    #         if self.board[d] == BORDER:
    #             at_edge = 1
    #         elif self.board[d] == opp_color:
    #             false_count += 1
    #     return false_count <= 1 - at_edge  # 0 at edge, 1 in center

    # def _is_surrounded(self, point, color):
    #     """
    #     check whether empty point is surrounded by stones of color
    #     (or BORDER) neighbors
    #     """
    #     for nb in self._neighbors(point):
    #         nb_color = self.board[nb]
    #         if nb_color != BORDER and nb_color != color:
    #             return False
    #     return True

    # def _has_liberty(self, block):
    #     """
    #     Check if the given block has any liberty.
    #     block is a numpy boolean array
    #     """
    #     for stone in where1d(block):
    #         empty_nbs = self.neighbors_of_color(stone, EMPTY)
    #         if empty_nbs:
    #             return True
    #     return False

    # def _block_of(self, stone):
    #     """
    #     Find the block of given stone
    #     Returns a board of boolean markers which are set for
    #     all the points in the block 
    #     """
    #     color = self.get_color(stone)
    #     assert is_black_white(color)
    #     return self.connected_component(stone)

    # def connected_component(self, point):
    #     """
    #     Find the connected component of the given point.
    #     """
    #     marker = np.full(self.maxpoint, False, dtype=bool)
    #     pointstack = [point]
    #     color = self.get_color(point)
    #     assert is_black_white_empty(color)
    #     marker[point] = True
    #     while pointstack:
    #         p = pointstack.pop()
    #         neighbors = self.neighbors_of_color(p, color)
    #         for nb in neighbors:
    #             if not marker[nb]:
    #                 marker[nb] = True
    #                 pointstack.append(nb)
    #     return marker

    # def _detect_and_process_capture(self, nb_point):
    #     """
    #     Check whether opponent block on nb_point is captured.
    #     If yes, remove the stones.
    #     Returns the stone if only a single stone was captured,
    #     and returns None otherwise.
    #     This result is used in play_move to check for possible ko
    #     """
    #     single_capture = None
    #     opp_block = self._block_of(nb_point)
    #     if not self._has_liberty(opp_block):
    #         captures = list(where1d(opp_block))
    #         self.board[captures] = EMPTY
    #         if len(captures) == 1:
    #             single_capture = nb_point
    #     return single_capture

    def play_move(self, point, color):
        """
        Play a move of color on point
        Returns boolean: whether move was legal
        """
        assert is_black_white(color)
        # Special cases
        if point == PASS:
            return True
        elif (self.get_empty_points().size == 0) or (self.board[point] != EMPTY):
            return False  

        self.board[point] = color
        return True
    
    def undo_move(self,point):
        '''
        Un - does move
        '''
        if self.board[point] == EMPTY:
            return False
        self.board[point]=EMPTY
        return True

    def neighbors_of_color(self, point, color):
        """ List of neighbors of point of given color """
        nbc = []
        for nb in self._neighbors(point):
            if self.get_color(nb) == color:
                nbc.append(nb)
        return nbc

    def _neighbors(self, point):
        """ List of all four neighbors of the point """
        return [point - 1, point + 1, point - self.NS, point + self.NS]

    def _diag_neighbors(self, point):
        """ List of all four diagonal neighbors of point """
        return [
            point - self.NS - 1,
            point - self.NS + 1,
            point + self.NS - 1,
            point + self.NS + 1,
        ]

    def last_board_moves(self):
        """
        Get the list of last_move and second last move.
        Only include moves on the board (not None, not PASS).
        """
        board_moves = []
        if self.last_move != None and self.last_move != PASS:
            board_moves.append(self.last_move)
        if self.last2_move != None and self.last2_move != PASS:
            board_moves.append(self.last2_move)
            return
 
    def get_result(self, color, move, win_condition):
        dirs = {"N":0, "S":0, "NE":0, "SW":0, "E":0, "W":0, "SE":0, "NW":0}
        check = 0
        for key in dirs:
            check += 1
            dirs[key] = self.check_direction(color, move, key)

            if check%2==0 and win_condition-1 <= \
                max(dirs["N"]+dirs["S"], dirs["NE"]+dirs["SW"], dirs["E"]+dirs["W"], dirs["SE"]+dirs["NW"]):
                if color == 1:
                    return "black"
                else:
                    return "white"

        if self.get_empty_points().size == 0:
            return "draw"
        return "unknown"

    def check_direction(self, color, pos, direction):
        increment = self.increments[direction]

        num = 0
        while self.get_color(pos+increment) == color:
            pos += increment
            num += 1

        return num