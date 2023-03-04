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
except:
	print("12: Connection erro.")
	sys.exit(1)

# Mensagem inicial do jogo
player_data = sock.recv(1024)
player = pickle.loads(player_data)
pNumber = player['pNumber']
color = player['color']
print(f'Bem vindo Jogador {pNumber}')
print(f'Você é a peça {color}.')

# Loop principal do jogo
while True:
    # Recebe o estado atual do jogo
    state_data = sock.recv(1024)
    state = pickle.loads(state_data)

    # Imprime o estado atual do jogo
    board = state['board']
    line = state['line']
    column = state['column']
    boardP= np.hstack((column,board))
    for row in boardP:
    	print(' '.join(row))
    for i in line:
       print(i, end = '   ')
    print(f'\n')
    

    # Pede a jogada ao usuário
    while True:
        
    	if state['next'] == 'white' and player['pNumber'] == 1:
        	print("Sua vez.")
        	try:
            		move_str = input("Digite a jogada (exemplo: e2 e4): ")
            		r1, c1, r2, c2 = move_str.split()
            		r1, c1, r2, c2 = int(r1) - 1, ord(c1) - ord('a'), int(r2) - 1, ord(c2) - ord('a')
            		move = (r1, c1, r2, c2)
            		break
        	except ValueError:
            		print("10:Jogada inválida.")
    	elif state['next'] == 'white' and player['pNumber'] == 2:
    		move = (0,0,0,0)
    		print("Eperando jogador white jogar.")
    		break
    
    	if state['next'] == 'black' and player['pNumber'] == 2:
        	print("Sua vez")
        	try:
            		move_str = input("Digite a jogada (exemplo: e2 e4): ")
            		r1, c1, r2, c2 = move_str.split()
            		r1, c1, r2, c2 = int(r1) - 1, ord(c1) - ord('a'), int(r2) - 1, ord(c2) - ord('a')
            		move = (r1, c1, r2, c2)
            		break
        	except ValueError:
            		print("10:Jogada inválida.")
    	elif state['next'] == 'black' and player['pNumber'] == 1:
    		move = (0,0,0,0)
    		print("Epperando jogador black jogar.")
    		break

    # Envia a jogada para o servidor
    move_data = pickle.dumps(move)
    sock.sendall(move_data)

