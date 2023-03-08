# client.py

import socket
import pickle
import sys
import numpy as np

HOST = '127.0.0.1'
PORT = 5003

# Cria o socket do cliente
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sock.connect((HOST, PORT))
	print("|              Xadrez                   |")
	print("| Peças brancas são em letra maiuscula. |")
	print("| Peças pretas são em letra minuscula.  |")
except:
	print("12: Connection error.")
	sys.exit(1)

# Mensagem inicial do jogo
player_data = sock.recv(1024)
player = pickle.loads(player_data)
pNumber = player['pNumber']
color = player['color']
turn_p = player['turn']
print(f'Bem vindo Jogador {pNumber}')
if player['color'] == 'white':
	print(f'Você é a peça branca.')
if player['color'] == 'black':
	print(f'Você é a peça preta.')

# Imprime o estado atual do jogo
def print_state(state):
    line = [' ','a','b','c','d','e','f','g','h']
    column = [['8'],['7'],['6'],['5'],['4'],['3'],['2'],['1']]
    boardP= np.hstack((column,state))
    for row in boardP:
    	print(' '.join(row))
    for i in line:
       print(i, end = ' ')
    print(f'\n')

# Recebe o estado atual do jogo
state_data = sock.recv(2048)
state = pickle.loads(state_data)
print_state(state)
    
turn_data = sock.recv(2048)
turn = pickle.loads(turn_data)
print(turn) #--> para debug

# Loop principal do jogo
while True:
    
    if turn == turn_p:
        move_str = input("Digite a jogada (exemplo: e2 e4): ")
        # Envia a jogada para o servidor
        move_data = pickle.dumps(move_str)
        sock.sendall(move_data)
    
    if turn != turn_p:
        print("Eperando...")
    
    # Recebe o estado atual do jogo
    state_data = sock.recv(2048)
    state = pickle.loads(state_data)
    print_state(state)
    
    turn_data = sock.recv(2048)
    turn = pickle.loads(turn_data)
    print(turn) #--> para debug
