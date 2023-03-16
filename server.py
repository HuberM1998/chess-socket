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
        piece, start_pos, end_pos = move

        # Checa se as coordenadas estão dentro do tabuleiro
        if start_pos[0] not in self.line or end_pos[0] not in self.line or \
           int(start_pos[1]) not in range(1, 9) or int(end_pos[1]) not in range(1, 9):
            return False

        start_col = self.line.index(start_pos[0])
        start_row = 8 - int(start_pos[1])

        end_col = self.line.index(end_pos[0])
        end_row = 8 - int(end_pos[1])

        # Checa se a posição inicial tem uma peça
        if self.board[start_row][start_col] != piece:
            return False

        # Checa se a posição final não tem uma peça da mesma cor
        if self.board[end_row][end_col].islower() == piece.islower():
            return False

        # Checa se o movimento é válido para o tipo de peça
        if not self._is_valid_move_for_piece(piece, start_row, start_col, end_row, end_col):
            return False

        return True
    
    def _is_valid_move_for_piece(self, piece, start_row, start_col, end_row, end_col):
        # Checa se o movimento é válido para um peão branco
        if piece == 'P':
            # Verifica se a peça está se movendo para frente
            if start_col == end_col and end_row == start_row - 1:
                # Checa se a posição final está livre
                if self.board[end_row][end_col] == ' ':
                    return True
            # Verifica se a peça está capturando uma peça inimiga na diagonal esquerda
            elif end_col == start_col - 1 and end_row == start_row - 1:
                if self.board[end_row][end_col].islower():
                    return True
            # Verifica se a peça está capturando uma peça inimiga na diagonal direita
            elif end_col == start_col + 1 and end_row == start_row - 1:
                if self.board[end_row][end_col].islower():
                    return True
            # Verifica se é o primeiro movimento do peão e pode andar duas casas para frente
            elif start_row == 6 and end_row == 4 and start_col == end_col and self.board[end_row][end_col] == ' ' and self.board[end_row + 1][end_col] == ' ':
                return True
            # Caso não seja nenhum dos movimentos válidos, retorna False
            else:
                return False
        # Checa se o movimento é válido para um peão preto
        elif piece == 'p':
            # Verifica se a peça está se movendo para frente
            if start_col == end_col and end_row == start_row + 1:
                # Checa se a posição final está livre
                if self.board[end_row][end_col] == ' ':
                    return True
            # Verifica se a peça está capturando uma peça inimiga na diagonal esquerda
            elif end_col == start_col - 1 and end_row == start_row + 1:
                if self.board[end_row][end_col].isupper():
                    return True
            # Verifica se a peça está capturando uma peça inimiga na diagonal direita
            elif end_col == start_col + 1 and end_row == start_row + 1:
                if self.board[end_row][end_col].isupper():
                    return True
            # Verifica se é o primeiro movimento do peão e pode andar duas casas para frente
            elif start_row == 1 and end_row == 3 and start_col == end_col and self.board[end_row][end_col] == ' ' and self.board[end_row - 1][end_col] == ' ':
                return True
            # Caso não seja nenhum dos movimentos válidos, retorna False
            else:
                return False

        # Checa se o movimento é válido para a torre branca ou preta
        if piece == 'R' or piece == 'r':
            # Verifica se a peça está se movendo em linha reta
            if start_row == end_row or start_col == end_col:
                # Verifica se há outras peças no caminho
                if start_row == end_row:
                    if start_col < end_col:
                        for col in range(start_col+1, end_col):
                            if self.board[start_row][col] != ' ':
                                return False
                    else:
                        for col in range(end_col+1, start_col):
                            if self.board[start_row][col] != ' ':
                                return False
                else:
                    if start_row < end_row:
                        for row in range(start_row+1, end_row):
                            if self.board[row][start_col] != ' ':
                                return False
                    else:
                        for row in range(end_row+1, start_row):
                            if self.board[row][start_col] != ' ':
                                return False
                # Verifica se a posição final está livre ou se há uma peça inimiga para capturar
                if self.board[end_row][end_col] == ' ' or (piece.isupper() != self.board[end_row][end_col].isupper()):
                    return True
                else:
                    return False
            else:
                return False
        
        # Checa se o movimento é válido para o bispo branco ou preto
        if piece == 'B' or piece == 'b':
            # Verifica se a peça está se movendo na diagonal
            if abs(start_row - end_row) == abs(start_col - end_col):
                # Verifica se há outras peças no caminho
                if end_row > start_row and end_col > start_col:
                    for i in range(1, end_row - start_row):
                        if self.board[start_row + i][start_col + i] != ' ':
                            return False
                elif end_row > start_row and end_col < start_col:
                    for i in range(1, end_row - start_row):
                        if self.board[start_row + i][start_col - i] != ' ':
                            return False
                elif end_row < start_row and end_col > start_col:
                    for i in range(1, start_row - end_row):
                        if self.board[start_row - i][start_col + i] != ' ':
                            return False
                elif end_row < start_row and end_col < start_col:
                    for i in range(1, start_row - end_row):
                        if self.board[start_row - i][start_col - i] != ' ':
                            return False
                # Verifica se a posição final está livre ou se há uma peça inimiga para capturar
                if self.board[end_row][end_col] == ' ' or (piece.isupper() != self.board[end_row][end_col].isupper()):
                    return True
                else:
                    return False
            else:
                return False

        # Checa se o movimento é válido para a rainha branca ou preta
        if piece == 'Q' or piece == 'q':
            # Verifica se a peça está se movendo em linha reta ou na diagonal
            if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
                # Verifica se há outras peças no caminho
                if start_row == end_row:
                    if start_col < end_col:
                        for col in range(start_col+1, end_col):
                            if self.board[start_row][col] != ' ':
                                return False
                    else:
                        for col in range(end_col+1, start_col):
                            if self.board[start_row][col] != ' ':
                                return False
                elif start_col == end_col:
                    if start_row < end_row:
                        for row in range(start_row+1, end_row):
                            if self.board[row][start_col] != ' ':
                                return False
                    else:
                        for row in range(end_row+1, start_row):
                            if self.board[row][start_col] != ' ':
                                return False
                elif abs(start_row - end_row) == abs(start_col - end_col):
                    if end_row > start_row and end_col > start_col:
                        for i in range(1, end_row - start_row):
                            if self.board[start_row + i][start_col + i] != ' ':
                                return False
                    elif end_row > start_row and end_col < start_col:
                        for i in range(1, end_row - start_row):
                            if self.board[start_row + i][start_col - i] != ' ':
                                return False
                    elif end_row < start_row and end_col > start_col:
                        for i in range(1, start_row - end_row):
                            if self.board[start_row - i][start_col + i] != ' ':
                                return False
                    elif end_row < start_row and end_col < start_col:
                        for i in range(1, start_row - end_row):
                            if self.board[start_row - i][start_col - i] != ' ':
                                return False
                # Verifica se a posição final está livre ou se há uma peça inimiga para capturar
                if self.board[end_row][end_col] == ' ' or (piece.isupper() != self.board[end_row][end_col].isupper()):
                    return True
                else:
                    return False

        # Checa se o movimento é válido para o cavalo branco ou preto
        if piece == 'N' or piece == 'n':
            # Verifica se a peça se move em L
            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
                if self.board[end_row][end_col] == ' ' or (piece.isupper() != self.board[end_row][end_col].isupper()):
                    return True
                else:
                    return False
            elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                if self.board[end_row][end_col] == ' ' or (piece.isupper() != self.board[end_row][end_col].isupper()):
                    return True
                else:
                    return False
            else:
                return False

        # Checa se o movimento é válido para o rei branco ou preto
        if piece == 'K' or piece == 'k':
            # Verifica se o rei se move apenas uma casa na horizontal ou vertical
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                # Checa se a posição final está livre ou com uma peça inimiga
                if self.board[end_row][end_col] == ' ' or (piece.isupper() and self.board[end_row][end_col].islower()) or (piece.islower() and self.board[end_row][end_col].isupper()):
                    return True
            # Caso não seja nenhum dos movimentos válidos, retorna False
            else:
                return False

    # Movimenta as peças
    def make_move(board, move):
        if len(move) != 3:
            return
        piece, start_pos, end_pos = move
        start_col = board.line.index(start_pos[0])
        start_row = 8 - int(start_pos[1])
        end_col = board.line.index(end_pos[0])
        end_row = 8 - int(end_pos[1])
        board.board[end_row][end_col] = piece
        board.board[start_row][start_col] = ' '
        return board
    
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