# chess.py

import numpy as np

# Auxiliary lists
col = ['a','b','c','d','e','f','g','h']
l = ['8','7','6','5','4','3','2','1']
black = ['r','p','n','b','q','k']
white = ['R','P','N','B','Q','K']

class Game():
	"""
		Game Class
	"""
	def __init__(self):
		self.board = Board()
		self.player1 = {'color': 'white', 'dead_pieces': []}
		self.player2 = {'color': 'black', 'dead_pieces': []}
		self.turn = True
	
	def reset_board():
		self.board.set_board()
		self.turn = True
	
	def update_turn(self,turn):
		self.turn = turn
	
	def get_turn(self):
		return self.turn
	
	def is_valid_move(self,move_from, move_to, board, piece):
		
		p = Piece(move_to,move_from,board)

		if piece == 'p' or piece == 'P':
			return p.is_valid_move_pawn(move_from, move_to, board, self.turn)
		if piece == 'b' or piece == 'B':
			return p.is_valid_move_bishop(move_from, move_to, board)
		if piece == 'k' or piece == 'K':
			return p.is_valid_move_king(move_from, move_to, board)
		if piece == 'q' or piece == 'Q':
			return p.is_valid_move_queen(move_from, move_to, board)
		if piece == 'r' or piece == 'R':
			return p.is_valid_move_rook(move_from, move_to, board)
		if piece == 'n' or piece == 'N':
			return p.is_valid_move_knight(move_from, move_to, board)
		
		return False
		
	def move(self,move_from,move_to):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from = i
			if move_to[0] == col[i]:
				num_to = i
		
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		b = self.board.get_board()
		
		if b[num_l_from][num_from] == ' ':
			print(f'6:Não há uma peça nesta posição.')
			return False
		
		piece = b[num_l_from][num_from]
		
		if self.check_piece_color(piece):
			print(f'4: Não é a sua peça')
			return False
		
		target = b[num_l_to][num_to]
		if piece.isupper() and target.isupper():
			print(f"5: Não pode comer sua própria peça.")
			return False
		if piece.islower() and target.islower():
			print(f'5: Não pode comer sua própria peça')
			return False
		
		if self.is_valid_move(move_from, move_to, b, piece):
			
			if target == ' ':
				b[num_l_from][num_from]	= ' '
				b[num_l_to][num_to] = piece
				self.board.update_board(b)						
			if target in black or target in white:
				b[num_l_from][num_from]	= ' ' 
				b[num_l_to][num_to] = piece
				self.board.update_board(b)
				
				if piece in black:
					self.player1['dead_pieces'].append(target)
				if piece in white:
					self.player2['dead_pieces'].append(target)
					
			if piece in white:
				turn = False
				self.update_turn(turn)
			elif piece in black:
				turn = True 
				self.update_turn(turn)
			return True
		else:
			print(f'8: Movimento inválido.')
			return False
		return True

	def check_piece_color(self,piece):
		if self.turn:
			if piece not in white:
				return True
		else:
			if piece not in black:
				return True
		return False
	
	# Verify input and split it in two lists: m_from and m_to
	def transform_input(self,move):
		m = move.split(' ')
		m_from = list(m[0])
		m_to = list(m[1])
		
		try:
			if int(m_from[1]) < 1 or int(m_from[1]) > 8:
				print(f"1: Não é um número entre 1 - 8.")
			if m_from[0] < 'a' or  m_from[0] > 'h':
				print(f'2: Não é uma letra entre a - h')
			return m_from, m_to
		except:
			print(f"3: {m_from} não está no formato certo: [letra][número]") 
			return None
		try:
			if int(m_to[1]) < 1 or int(m_to[1]) > 8:
				print(f"1: Não é um número entre 1 - 8.")
			if m_to[0] < 'a' or  m_to[0] > 'h':
				print(f'2: Não é uma letra entre a - h')
			return m_from, m_to
		except:
			print(f"3: {m_to} não está no formato certo: [letra][número]") 
			return None
		
		return None

	def getDead_pieces(self,player):
		return self.player['dead_pieces']
	
class Board():
	"""
		Board Class.
	"""
	def __init__(self):
		self.line = [' ','a','b','c','d','e','f','g','h']
		self.column = [['8'],['7'],['6'],['5'],['4'],['3'],['2'],['1']]
		self.board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
			      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                              ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
	def print_board(self):
		boardP= np.hstack((self.column,self.board))
		for row in boardP:
			print(' '.join(row))
		for i in self.line:
			print(i, end = ' ')
		print(f'\n')
	
	def get_board(self):
		return self.board
	
	def update_board(self,board):
		self.board = board
	
	def set_board(self):
		self.board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
			      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                              ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                              ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

class Piece():
	"""
		Piece Class
		
		Rook = Can only move horizontally nd vertically
		Queen = Can move in all directions
		King = Can move one square in all directions
		Pawn = Can only move two squares in the first move. AFter it can move one square foward.
		Knight = Can only move L shaped (2 squares, 1 square) in any direction
		BIshop = Can only move diagonally
		
	"""
	def __init__(self,move_to,move_from,board):
		self.move_to = move_to
		self.move_from = move_from
		self.board = board
	
	def is_valid_move_rook(self,move_from, move_to, board):
		if int(move_from[1]) == int(move_to[1]) or move_from[0] == move_to[0]:
			return self.check_updown(move_from, move_to,board)
		print(f'8: Movimento inválido.')
		return False
		
	def is_valid_move_bishop(self,move_from,move_to,board):
		return self.check_diagonal(move_from,move_to,board)

	def is_valid_move_queen(self,move_from,move_to,board):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i
		
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if abs(num_from_ - num_to) == abs(num_l_from - num_l_to):
			return self.check_diagonal(move_from,move_to,board)			
		
		if num_from_ == num_to or num_l_from == num_l_to:
			return self.check_updown(move_from,move_to,board)
		
		print(f'8: Movimento inválido.')
		return False
	
	def is_valid_move_king(self,move_from,move_to,board):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i
		
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if abs(num_l_from - num_l_to) > 1:
			print(f'8: Movimento Inválido')
			return False 
		if abs(num_from_ - num_to) > 1:
			print(f'8: Movimento Inválido')
			return False 

		return True		

	def is_valid_move_knight(self,move_from,move_to,board):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i		
		
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if abs(num_from_ - num_to) == 2 and abs(num_l_from - num_l_to) == 1:
			return True			
		if abs(num_from_ - num_to) == 1 and abs(num_l_from - num_l_to) == 2:
			return True
		
		print(f'8: Movimento inválido.')
		return False

	def is_valid_move_pawn(self,move_from,move_to,board,turn):
	
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i
				
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i	
					
		target = board[num_l_to][num_to]
		
		if num_from_ != num_to: 
			if target in white or target in black:
				if abs(num_l_from - num_l_to) == 1 and abs(num_from_ - num_to) == 1:
					return True 

			print(f'8: Movimento Inválido.')
			return False
		
		piece = board[num_l_from][num_from_]
		
		if self.pawn_behind(piece,num_l_from,num_l_to,turn):
			print(f'8: Movimento Inválido.')
			return False			
		
		if num_l_from == 1 or num_l_from == 6:
			if abs(num_l_from - num_l_to) > 2:
				print(f'8: Movimento Inválido.')
				return False
			return True
		else:
			if abs(num_l_from - num_l_to) > 1:
				print(f'Movimento Inválido.')
				return False
			return True
			
		return True
		
	# Verifies if pawn is being moved to a position "below" it  
	def pawn_behind(self,piece, num_l_from, num_l_to,turn):
		if turn:
			if piece in white:
				if num_l_from - num_l_to < 0:
					print(f'8: Moviento Inválido.')
					return True
		else:
			if piece in black:
				if num_l_from - num_l_to > 0:
					print(f'8: Moviento Inválido.')
					return True
		return False
	
	
	# Check if there is one or more pieces in the middle of the way in the horizontal or vertical direction
	def check_updown(self,move_from, move_to, board):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i
				
		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if move_from[1] == move_to[1]:
			smaller_y = num_from_ if num_from_ < num_to else num_to
			bigger_y =  num_from_ if num_from_ > num_to else num_to
			
			for i in range(smaller_y +1, bigger_y):
				if board[num_l_from][i] != ' ':
					print(f'13: Caminho bloqueado.')
					return False
			return True
		else:
			smaller_x = (num_l_from) if (num_l_from) < (num_l_to) else (num_l_to)
			bigger_x =  (num_l_from) if (num_l_from) > (num_l_to) else (num_l_to)
			
			for i in range(smaller_x +1, bigger_x):
				if board[i][num_from_] != ' ':
					print(f'13: Caminho bloqueado.')
					return False
			return True
	
	# Check if there is one or more pieces in the middle of the way in the diagonal 
	def check_diagonal(self,move_from,move_to,board):
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i

		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if  abs( num_l_from - num_l_to) != abs( num_from_ - num_to):
			print(f'8: Movimento Inválido.')
			return False
		
		x = 1 if (num_l_to) - (num_l_from) > 0 else -1
		y = 1 if num_to - num_from_ > 0 else -1
		
		i =  (num_l_from) + x
		j =  num_from_ + y
		
		while(i < num_l_to if x==1 else i > num_l_to):
			if board[i][j] != ' ':
				print(f'13: Caminho bloqueado.')
				return False
			i += x
			j += y
		
		return True
	
	def king_check(self,move_from,move_to,board,turn):

		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i

		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		###
		
		return False
	
	# Knight
	def check_knight(self, board, turn, pos):
		
		piece = board[pos[0]][pos[1]]
		if turn == True:
			if piece != ' ' and piece not in white and piece == 'n':
				return False
			return True
		elif turn == False:
			if piece != ' ' and piece not in black and piece == 'N':
				return False
			return True
	
	# Rook and Queen
	def check_UD(self, num_from_, num_l_from, board,turn):
		
		king = [ num_l_from , num_from_ ]
		
		if turn == True:
			for i in range(8):
				for j in range(8):
					if i == num_l_from:
						if board[i][j] == 'q':
							temp = abs(j - num_from_)
							while temp != 0:
								if board[i][temp] in black or board[i][temp] in white:
									return False
								temp -=1
							return True
						if board[i][j] == 'r':
							temp = abs(j - num_from_)
							while temp != 0:
								if board[i][temp] in black or board[i][temp] in white:
									return False
								temp -=1
							return True
					if j == num_from_ :
						if board[i][j] == 'q':
							temp = abs(i - num_l_from)
							while temp != 0:
								if board[temp][j] in black or board[temp][j] in white:
									return False
								temp -=1
							return True
						if board[i][j] == 'r':
							temp = abs(i - num_l_from)
							while temp != 0:
								if board[temp][j] in black or board[temp][j] in white:
									return False
								temp -=1
							return True
		elif turn == False:
			for i in range(8):
				for j in range(8):
					if i == num_l_from:
						if board[i][j] == 'Q':
							temp = abs(j - num_from_)
							while temp != 0:
								if board[i][temp] in black or board[i][temp] in white:
									return False
								temp -=1
							return True
							
						if board[i][j] == 'R':
							temp = abs(j - num_from_)
							while temp != 0:
								if board[i][temp] in black or board[i][temp] in white:
									return False
								temp -=1
							return True
					if j == num_from_ :
						if board[i][j] == 'Q':
							temp = abs(i - num_l_from)
							while temp != 0:
								if board[temp][j] in black or board[temp][j] in white:
									return False
								temp -=1
							return True
							
						if board[i][j] == 'R':
							temp = abs(i - num_l_from)
							while temp != 0:
								if board[temp][j] in black or board[temp][j] in white:
									return False
								temp -=1
							return True
		
	# Pawn, Bishop and Queen
	def check_HV(self, move_to,move_from, board,turn):
		
		for i in range(len(col)):
			if move_from[0] == col[i]:
				num_from_ = i
			if move_to[0] == col[i]:
				num_to = i

		for i in range(len(l)):
			if move_from[1] == l[i]:
				num_l_from = i
			if move_to[1] == l[i]:
				num_l_to = i
		
		if turn == True:
			x = 1 if num_l_to - num_l_from > 0 else -1 
			y = 1 if num_to - num_from_ > 0 else -1
			
			i = num_l_from + x
			j = num_from_ + y
			
			exist = board[i][j] != None
			if exist and board[i][j] not in white: 
				return False
			
			while( i <= num_l_to if x == 1 else i >= num_l_to):
				if exist and board[i][j] not in white:
					if board[i][j] in black:
						return False	
					else:
						return True
				if exist and board[i][j] in white:
					return True
				
				i += x
				j += y
				exist = board[i][j] != None
			return True
		elif turn == False:
			x = 1 if num_l_to - num_l_from > 0 else -1 
			y = 1 if num_to - num_from_ > 0 else -1
			
			i = num_l_from + x
			j = num_from_ + y
			
			exist = board[i][j] != None
			if exist and board[i][j] not in black: 
				return False
			
			while( i <= num_l_to if x == 1 else i >= num_l_to):
				if exist and board[i][j] not in black:
					if board[i][j] in white:
						return False	
					else:
						return True
				if exist and board[i][j] in black:
					return True
				
				i += x
				j += y
				exist = board[i][j] != None
			return True

"""
if __name__ == "__main__":
	chess = Game()
	chess.board.print_board()
	
	
	while True:
		move = input("Sua jogada - de para - (exemplo: e2 e4): ")		
		print(list(move))
		if len(list(move)) != 5:
			print(f'7: Formato de entrada incorreto. Formato: e2 e4')
		
		move_from, move_to = chess.transform_input(move)	
				
		chess.move(move_from,move_to)
		
		chess.board.print_board()
"""
