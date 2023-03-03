# client.py

import socket
import pickle

HOST = '127.0.0.1'
PORT = 5003

# Cria o socket do cliente
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Loop principal do jogo
while True:
    # Recebe o estado atual do jogo
    state_data = sock.recv(1024)
    state = pickle.loads(state_data)

    # Imprime o estado atual do jogo
    board = state['board']
    for row in board:
        print(' '.join(row))
    if state['white_to_move']:
        print("Branco é o próximo a jogar.")
    else:
        print("Preto é o próximo a jogar.")

    # Pede a jogada ao usuário
    while True:
        #corrigir
        try:
            move_str = input("Digite a jogada (exemplo: e2 e4): ")
            r1, c1, r2, c2 = move_str.split()
            r1, c1, r2, c2 = int(r1) - 1, ord(c1) - ord('a'), int(r2) - 1, ord(c2) - ord('a')
            move = (r1, c1, r2, c2)
            break
        except ValueError:
            print("Jogada inválida.")

    # Envia a jogada para o servidor
    move_data = pickle.dumps(move)
    sock.sendall(move_data)
