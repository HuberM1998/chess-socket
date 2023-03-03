# server.py

import socket
import pickle

HOST = '127.0.0.1'
PORT = 5003

# Classe para representar o tabuleiro de xadrez
class Board:
    def __init__(self):
        self.board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                      [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
                      ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
                      [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
                      ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                      ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self.white_to_move = True

    def make_move(self, move):
        # Converte as coordenadas do movimento em índices da matriz
        r1, c1, r2, c2 = move
        # Realiza o movimento
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = ' '
        self.white_to_move = not self.white_to_move

    def get_state(self):
        # Retorna o estado atual do jogo em formato de dicionário
        return {'board': self.board, 'white_to_move': self.white_to_move}


# Inicializa o tabuleiro
board = Board()

# Cria o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

# Aguarda a conexão dos clientes
print('Aguardando conexões...')
conn1, addr1 = sock.accept()
print(f'Cliente 1 conectado: {addr1}')
conn2, addr2 = sock.accept()
print(f'Cliente 2 conectado: {addr2}')

# Loop principal do jogo
while True:
    # Envia o estado atual do jogo para os clientes
    state1 = pickle.dumps(board.get_state())
    conn1.sendall(state1)
    state2 = pickle.dumps(board.get_state())
    conn2.sendall(state2)

    # Recebe a jogada do jogador 1
    move1_data = conn1.recv(1024)
    move1 = pickle.loads(move1_data)
    board.make_move(move1)

    # Recebe a jogada do jogador 2
    move2_data = conn2.recv(1024)
    move2 = pickle.loads(move2_data)
    board.make_move(move2)