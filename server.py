# server.py

import socket
import pickle

HOST = '127.0.0.1'
PORT = 5003

# Classe para representar o tabuleiro de xadrez
class Board:
    def __init__(self):
    	self.line = [' ','a','b','c','d','e','f','g','h']
    	self.column = [['1'],['2'],['3'],['4'],['5'],['6'],['7'],['8']]
    	self.board = [['r_b', 'n_b', 'b_b', 'q_b', 'k_b', 'b_b', 'n_b', 'r_b'],
                      ['p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b'],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      ['P_w', 'P_w', 'P_w', 'P_w', 'P_w', 'P_w', 'P_w', 'P_w'],
                      ['R_w', 'N_w', 'B_w', 'Q_w', 'K_w', 'B_w', 'N_w', 'R_w']]
    	self.next = 'white'
    	
    def update(self,next):
    	self.next = next
    
    def make_move(self, move):
        pass
    
    def end_game(self):
    	pass

    def get_state(self):
        # Retorna o estado atual do jogo em formato de dicionário
        return {'board': self.board, 'next': self.next, 'line': self.line, 'column': self.column}
	
# Classe representa os jogadores
class Player:
	def __init__(self, color, pNumber):
		self.color = color
		self.pNumber = pNumber
	
	def getPlayer(self):
		return {'color': self.color, 'pNumber': self.pNumber}
	
# Inicializa o tabuleiro
board = Board()

# Inicializa os jogadores
player1 = Player('white',1)
player2 = Player('black',2)

# Cria o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

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
    	move1_data = conn1.recv(1024)
    	move1 = pickle.loads(move1_data)
    	board.make_move(move1)
    	board.update('black')
    	
    if next_state['next'] == 'black':
    	# Recebe a jogada do jogador 2
    	move2_data = conn2.recv(1024)
    	move2 = pickle.loads(move2_data)
    	board.make_move(move2)
    	board.update('white')

sock.shutdown()
sock.close()
