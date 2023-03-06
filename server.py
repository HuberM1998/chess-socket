# server.py

import socket
import pickle
from enum import Enum

HOST = '127.0.0.1'
PORT = 5003

# Cria o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

# Enumera a posição das colunas do tabuleiro
col = ('a','b','c','d','e','f','g','h')
	
# Classe para representar o jogo
class Board:
    def __init__(self):
    	self.next = 'white'
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
    
    # Faz um update de next, mudando quem pode jogar
    def update(self,next):
    	self.next = next
    
    # Verifica se o movimento é valido
    def is_valid_move(self, move):
    	
    	pass
    
    # Movimenta as peças
    def make_move(self, move):
    	pass
    
    # Define fim de jogo
    def end_game(self):
    	pass
    
    # Retorna o estado atual do jogo em formato de dicionário
    def get_state(self):
        return {'board': self.board, 'next': self.next, 'line': self.line, 'column': self.column}

# Classe representa os jogadores
class Player:
	def __init__(self, color, pNumber):
		self.color = color
		self.pNumber = pNumber
		self.dead_pieces = []
	
	def getPlayer(self):
		return {'color': self.color, 'pNumber': self.pNumber}

	def dead_pieces(self, piece):
		self.dead_pieces.append(piece)
		pass
		
# Inicializa o tabuleiro
board = Board()

# Inicializa os jogadores
player1 = Player('white',1)
player2 = Player('black',2)

# Aguarda a conexão dos clientes
print('Aguardando conexões...')

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

# Loop principal do jogo
while True:
    # Envia o estado atual do jogo para os clientes
    state1 = pickle.dumps(board.get_state())
    conn1.sendall(state1)
    state2 = pickle.dumps(board.get_state())
    conn2.sendall(state2)

    next_state = board.get_state()
    if next_state['next'] == 'white':
    	# Recebe a jogada do jogador 1
    	move1_data = conn1.recv(2048)
    	move1 = pickle.loads(move1_data)
    	board.make_move(move1)
    	board.update('black')
    
    elif next_state['next'] == 'black':
    	# Recebe a jogada do jogador 2
    	move2_data = conn2.recv(2048)
    	move2 = pickle.loads(move2_data)
    	board.make_move(move2)
    	board.update('white')

sock.shutdown()
sock.close()
