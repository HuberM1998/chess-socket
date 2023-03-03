import socket
import threading

# Define a porta e o endereço do servidor
HOST = '127.0.0.1'
PORT = 5000

# Inicializa o socket do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Armazena as conexões dos clientes
clients = []

# Define a classe para representar o jogo de xadrez
class ChessGame:
    def __init__(self):
        # Inicializa o tabuleiro
        self.board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [" ", ".", " ", ".", " ", ".", " ", "."],
            [".", " ", ".", " ", ".", " ", ".", " "],
            [" ", ".", " ", ".", " ", ".", " ", "."],
            [".", " ", ".", " ", ".", " ", ".", " "],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]
        self.turn = "white"

    # Verifica se um movimento é válido
def is_valid_move(self, from_square, to_square):
    # Obtem a peça que será movida e as coordenadas de origem e destino
    piece = self.board[from_square[0]][from_square[1]]
    r1, c1 = from_square
    r2, c2 = to_square

    # Verifica se a peça pertence ao jogador atual
    if piece.isupper() and self.current_player == 'white' or \
       piece.islower() and self.current_player == 'black':
        return False

    # Verifica se o movimento é válido para a peça
    if piece.lower() == 'p':
        if self._is_valid_pawn_move(r1, c1, r2, c2):
            return True
    elif piece.lower() == 'r':
        if self._is_valid_rook_move(r1, c1, r2, c2):
            return True
    elif piece.lower() == 'n':
        if self._is_valid_knight_move(r1, c1, r2, c2):
            return True
    elif piece.lower() == 'b':
        if self._is_valid_bishop_move(r1, c1, r2, c2):
            return True
    elif piece.lower() == 'q':
        if self._is_valid_queen_move(r1, c1, r2, c2):
            return True
    elif piece.lower() == 'k':
        if self._is_valid_king_move(r1, c1, r2, c2):
            return True

    # O movimento não é válido
    return False


    # Executa um movimento
    def make_move(self, from_square, to_square):
        # Implemente aqui a lógica para executar um movimento
        pass

# Define a função para lidar com as conexões dos clientes
def handle_client(conn, addr, game):
    print(f"Nova conexão: {addr}")
    clients.append(conn)

    while True:
        # Recebe os dados do cliente
        data = conn.recv(1024).decode()
        if not data:
            print(f"Cliente desconectado: {addr}")
            clients.remove(conn)
            break

        # Processa os dados recebidos
        parts = data.strip().split(" ")
        if len(parts) != 2:
            print(f"Comando inválido do cliente {addr}: {data}")
            continue

        from_square, to_square = parts
        if not game.is_valid_move(from_square, to_square):
            print(f"Jogada inválida do cliente {addr}: {data}")
            continue

        game.make_move(from_square, to_square)
        for c in clients:
            c.send(f"{from_square} {to_square}".encode())

    conn.close()

# Inicializa o jogo e começa a aceitar conexões dos clientes
game = ChessGame()
print("Servidor de xadrez iniciado")

while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr, game))
    t.start()