# chess.py - server.py

import socket
import pickle
import numpy as np

HOST = '127.0.0.1'
PORT = 5003

# Auxiliary lists
col = ['a','b','c','d','e','f','g','h']
l = ['8','7','6','5','4','3','2','1']
black = ['r','p','n','b','q','k']
white = ['R','P','N','B','Q','K']

class Game():
	"""
		Game Class
	"""
	def __init__(self,player1,player2):
		self.board = Board()
		self.player1 = player1
		self.player2 = player2
		self.turn = True
			
	def promotion(self):
		# Promotes the Pawn
		pass
	
	def update_turn(self,turn):
		self.turn = turn
	
	def get_turn(self):
		return self.turn
	
	def is_valid_move(self,move_from, move_to, board, piece):
		
		p = Piece(move_to,move_from,board)

		if piece == 'p' or piece == 'P':
			return p.is_valid_move_pawn(move_from, move_to, board)
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
			return
		
		piece = b[num_l_from][num_from]
		
		if self.check_piece_color(piece):
			print(f'4: Não é a sua peça')
			return
		
		target = b[num_l_to][num_to]
		if piece.isupper() and target.isupper():
			print(f"5: Não pode comer sua própria peça.")
			return
		if piece.islower() and target.islower():
			print(f'5: Não pode comer sua própria peça')
			return
		
		
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
					self.player1.dead_pieces(target)
				if piece in white:
					self.player2.dead_pieces(target)
				
			if piece in white:
				turn = False
				self.update_turn(turn)
			elif piece in black:
				turn = True 
				self.update_turn(turn)
		else:
			print(f'8: Movimento inválido.')
			return
	
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

class Player():
	"""
		Player Class
	"""
	def __init__(self, color, pNumber,turn):
		self.color = color
		self.pNumber = pNumber
		self.turn = turn
		self.dead_pieces = []
	
	def getPlayer(self):
		return {'color': self.color, 'pNumber': self.pNumber, 'turn': self.turn}

	def dead_pieces(self, piece):
		self.dead_pieces.append(piece)
		
	def list_deadpieces(self):
		for i in self.dead_pieces:
			print(f'{i}: {dead_pieces[i]}')
	
	def getDead_pieces(self):
		return self.dead_pieces

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
		
		# TO DO CHECK CONDITIONS
		
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

	def is_valid_move_pawn(self,move_from,move_to,board):
	
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
		
		if num_from_ != num_to:
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
		
		if  abs( num_l_from - num_l_to) != abs( num_from_ - num_to) :
			print(f'8: Movimento Inválido.')
			return
		
		x = 1 if (num_l_to) - (num_l_from) > 0 else -1
		y = 1 if num_to - num_from_ > 0 else -1
		
		i =  (num_l_from) + x
		j =  num_from_ + y
		
		if x == 1:
			i < (num_l_to)
		else:
			i > (num_l_to)
		
		while(i):
			if board[i][j] != ' ':
				print(f'13: Caminho bloqueado.')
				return False
			i += x
			j += y
	
	# --
	def king_check(self,move_from,move_to,board):

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
		
		# TO DO
		
		return False
		
if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((HOST, PORT))
	sock.listen(2)
	# Aguarda a conexão dos clientes
	print('Aguardando conexões...')
	
	player1 = Player('white',1, True)
	player2 = Player('black',2, False)
	chess = Game(player1,player2)
	
	# Jogador 1
	conn1, addr1 = sock.accept()
	print(f'Cliente 1 conectado: {addr1}')

	# Jogador 2
	conn2, addr2 = sock.accept()
	print(f'Cliente 2 conectado: {addr2}')
	
	# Mensagem inicial do jogo
	welcome1 = pickle.dumps(player1.getPlayer())
	conn1.sendall(welcome1)
	welcome2 = pickle.dumps(player2.getPlayer())
	conn2.sendall(welcome2)

	b = chess.board.get_board()
	b1 = pickle.dumps(b)
	conn1.sendall(b1)
	b2 = pickle.dumps(b)
	conn2.sendall(b2)
	
	turn = chess.get_turn()
	t1 = pickle.dumps(turn)
	conn1.sendall(t1)
	t2 = pickle.dumps(turn)
	conn2.sendall(t2)
	
	while True:
		if chess.get_turn() == True:
			# Recebe a jogada do jogador 1
    			move1_data = conn1.recv(2048)
    			move1 = pickle.loads(move1_data)
    			#print(move1) --> para debug
    			if len(list(move1)) != 5:
    				print(f'7: Formato de entrada incorreto. Formato: e2 e4')
    			move_from, move_to = chess.transform_input(move1)
    			chess.move(move_from,move_to)
		elif chess.get_turn() == False:
			# Recebe a jogada do jogador 2
    			move2_data = conn2.recv(2048)
    			move2 = pickle.loads(move2_data)
    			#print(move2) --> para debug
    			if len(list(move2)) != 5:
    				print(f'7: Formato de entrada incorreto. Formato: e2 e4')
    			move_from, move_to = chess.transform_input(move2)
    			chess.move(move_from,move_to)
		
		turn = chess.get_turn()
		t1 = pickle.dumps(turn)
		conn1.sendall(t1)
		t2 = pickle.dumps(turn)
		conn2.sendall(t2)
		
		b = chess.board.get_board()
		b1 = pickle.dumps(b)
		conn1.sendall(b1)
		b2 = pickle.dumps(b)
		conn2.sendall(b2)
	
	sock.shutdown()
	sock.close()
