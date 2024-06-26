import math
import numpy as np
import random
import sys


from tkinter import *



BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7


EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


class Connect4Engine():

	def __init__(self):





		self.board = self.create_board()

	def create_board(self):
		board = np.zeros((ROW_COUNT,COLUMN_COUNT))
		return board

	def drop_piece(self, board, row, col, piece):
		board[row][col] = piece

	def is_valid_location(self, board, col):
		return board[ROW_COUNT-1][col] == 0

	def get_next_open_row(self, board, col):
		for r in range(ROW_COUNT):
			if board[r][col] == 0:
				return r

	def print_board(self, board):
		print(np.flip(board, 0))

	def winning_move(self, board, piece):
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
					return True


		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
					return True



	def evaluate_window(self, window, piece):
		score = 0
		opp_piece = PLAYER_PIECE
		if piece == PLAYER_PIECE:
			opp_piece = AI_PIECE

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
			score -= 4

		return score

	def score_position(self, board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(ROW_COUNT):
			row_array = [int(i) for i in list(board[r,:])]
			for c in range(COLUMN_COUNT-3):
				window = row_array[c:c+WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score Vertical
		for c in range(COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:,c])]
			for r in range(ROW_COUNT-3):
				window = col_array[r:r+WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score posiive sloped diagonal
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		return score

	def is_terminal_node(self, board):
		return self.winning_move(board, PLAYER_PIECE) or self.winning_move(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

	def minimax(self, board, depth, alpha, beta, maximizingPlayer, ai_piece, player_piece):
		valid_locations = self.get_valid_locations(board)
		is_terminal = self.is_terminal_node(board)
		if depth == 0 or is_terminal:
			if is_terminal:
				if self.winning_move(board, ai_piece):
					return (None, float('inf'))
				elif self.winning_move(board, player_piece):
					return (None, -float('inf'))
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, self.score_position(board, ai_piece))
		if maximizingPlayer:
			value = -float('inf')
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.get_next_open_row(board, col)
				b_copy = board.copy()
				self.drop_piece(b_copy, row, col, ai_piece)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, False, ai_piece, player_piece)[1]
				if new_score > value:
					value = new_score
					column = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value

		else: # Minimizing player
			value = float('inf')
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.get_next_open_row(board, col)
				b_copy = board.copy()
				self.drop_piece(b_copy, row, col, player_piece)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, True, ai_piece, player_piece)[1]
				if new_score < value:
					value = new_score
					column = col
				beta = min(beta, value)
				if alpha >= beta:
					break
			return column, value

	def get_valid_locations(self, board):
		valid_locations = []
		for col in range(COLUMN_COUNT):
			if self.is_valid_location(board, col):
				valid_locations.append(col)
		return valid_locations