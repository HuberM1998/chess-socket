import socket
import threading

# Define a porta e o endereço do servidor
HOST = '127.0.0.1'
PORT = 5000

# Inicializa o socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Define a função para receber atualizações do servidor
def receive_updates():
    while True:
        # Recebe os dados do servidor
        data = client.recv(1024).decode()
        if not data:
            print("Servidor desconectado")
            break

        # Processa os dados recebidos
        from_square, to_square = data.strip().split(" ")
        print(f"Oponente moveu de {from_square} para {to_square}")

# Inicia uma nova thread para receber atualizações do servidor
t = threading.Thread(target=receive_updates)
t.start()

# Loop principal do cliente
while True:
    # Exibe o tabuleiro
    print("Tabuleiro:")
    for row in game.board:
        print(" ".join(row))
    print(f"Vez das {game.turn}")

    # Recebe a jogada do jogador
    from_square = input("De: ")
    to_square = input("Para: ")

    # Envia a jogada para o servidor
    client.send(f"{from_square} {to_square}".encode())