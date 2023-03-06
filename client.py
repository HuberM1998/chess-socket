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
print(f'Bem vindo Jogador {pNumber}')
print(f'Você é a peça {color}.')

# Imprime o estado atual do jogo
def print_state(state):
    board = state['board']
    line = state['line']
    column = state['column']
    boardP= np.hstack((column,board))
    for row in boardP:
    	print(' '.join(row))
    for i in line:
       print(i, end = ' ')
    print(f'\n')

# Loop principal do jogo
while True:
    # Recebe o estado atual do jogo
    state_data = sock.recv(2048)
    state = pickle.loads(state_data)
    print_state(state)

    # Pede a jogada ao usuário
    while True:
        
    	if state['next'] == 'white' and player['pNumber'] == 1:
        	print("Sua vez.")
        	try:
            		move_str = input("Digite a jogada (exemplo: P e4): ")
            		move = move_str
            		break
        	except ValueError:
            		print("10:Jogada inválida.")
    	elif state['next'] == 'white' and player['pNumber'] == 2:
    		move = ' '
    		print("Eperando jogador jogar.")
    		break
    
    	if state['next'] == 'black' and player['pNumber'] == 2:
        	print("Sua vez.")
        	try:
            		move_str = input("Digite a jogada (exemplo: p e4): ")
            		move = move_str
            		break
        	except ValueError:
            		print("10:Jogada inválida.")
    	elif state['next'] == 'black' and player['pNumber'] == 1:
    		move = ' '
    		print("Esperando jogador jogar.")
    		break

    # Envia a jogada para o servidor
    move_data = pickle.dumps(move)
    sock.sendall(move_data)

