import socket
import pickle
import numpy as np
import chess

def connect_client():
	HOST = "127.0.0.1"
	PORT = 5000
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Conectando cliente ao servidor ...")
	client.connect((HOST, PORT))
	print("Conectado ao servidor!")

	while True:
		fs = client.recv(2048*2)
		from_server = pickle.loads(fs)
		
		if not from_server:
			break
		
		if from_server.startswith("welcome"):
			if from_server == "welcome1":
				print("Bem vindo jogador 1")
				print("|              Xadrez                   |")
				print("| Peças brancas são em letra maiuscula. |")
				print("| Peças pretas são em letra minuscula.  |")
				print("| Você é a branca.                      |")
				print("| Digite: desistir para recomeçar jogo  |")
				ready = 'ready'
				client.sendall(pickle.dumps(ready))
			elif from_server == "welcome2":
				print("Bem vindo jogador 2")
				print("|              Xadrez                   |")
				print("| Peças brancas são em letra maiuscula. |")
				print("| Peças pretas são em letra minuscula.  |")
				print("| Você é a preta.                       |")
				print("| Digite: desistir para recomeçar jogo  |")
				ready = 'ready'
				client.sendall(pickle.dumps(ready))
		
		elif from_server.startswith("start"):
			print("Jogo vai começar.")  
			game_begin = from_server.split('\n')
			print_state(game_begin[1])
			print(type(game_begin[2]))
			if game_begin[2] == 'True':
				move = input("Faça seu movimento (ex. e2 e4): ")
				
				if move == 'desistir':
					client.sendall(pickle.dumps('give up'))
				else:
					while len(list(move)) != 5:
						print(f'7: Formato de entrada incorreto. Formato: e2 e4')
						move = input("Faça seu movimento (ex. e2 e4): ")
					mm = 'send move' + '\n' + move
					client.sendall(pickle.dumps(mm))
	
			else:
				print("Esperano jogador adversário.")
				client.sendall(pickle.dumps('wait'))
				
		elif from_server.startswith("update"):
			board = from_server.split('\n')
			print_state(board[1])
			if board[2] == 'current':
				move = input("Faça seu movimento (ex. e2 e4): ")
				
				if move == 'desistir':
					client.sendall(pickle.dumps('give up'))				
				else:
					while len(list(move)) != 5:
						print(f'7: Formato de entrada incorreto. Formato: e2 e4')
						move = input("Faça seu movimento (ex. e2 e4): ")
					mm = 'send move' + '\n' + move
					client.sendall(pickle.dumps(mm))
			else:
				print("Esperando jogador adversário.")
				client.sendall(pickle.dumps('wait'))
			
		elif from_server.startswith('OK'):
			print('Jogada aceita')
		
		elif from_server.startswith('invalid'):
			print('Jogada inválida.')
			move = input("Faça seu movimento (ex. e2 e4): ")
			
			if move == 'desistir':
				client.sendall(pickle.dumps('give up'))
			else:
				while len(list(move)) != 5:
					print(f'7: Formato de entrada incorreto. Formato: e2 e4')
					move = input("Faça seu movimento (ex. e2 e4): ")
				mm = 'send move' + '\n' + move
				client.sendall(pickle.dumps(mm))
			
		elif from_server.startswith('wait'):
			print("Esperando jogador adversário.")
			client.sendall(pickle.dumps('wait'))
				
		elif from_server.startswith("check mate"):
			print("Jogador" + color + "venceu")
			choice = input("Quer começar nova partida?(SIM ou NAO): ")
			client.sendall(pickle.dumps('start again' + '\n' + choice))
			
		elif from_server.startswith("game end"):
			print("Um jogador desistiu. Partida será reiniciada!")
			choice = input("Quer começar nova partida?(SIM ou NAO): ")
			client.sendall(pickle.dumps('start again' + '\n' + choice))
		
		elif from_server.startswith("end conn"):
			print("Conexão com servidor será encerrada.")
			client.close()
			
	client.close()

# Imprime o estado atual do jogo
def print_state(state):
	line = [' ','a','b','c','d','e','f','g','h']
	column = [['8'],['7'],['6'],['5'],['4'],['3'],['2'],['1']]
	board = convert_string_board(state)
	bP = np.hstack((column,board))
	for row in bP:
		print(' '.join(row))
	for i in line:
		print(i, end = '  ')
	print(f'\n')

# Converte o tabuleiro
def convert_string_board(state):
	s3 = state.replace("[", "").replace("]", "").replace("'", "").replace(" ", " ")
	s4 = s3.split(",")
	board = [[],[],[],[],[],[],[],[]]
	
	for i in range(len(s4)):
		if (i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6 or i == 7):
			board[0].append(s4[i])
		if (i == 8 or i == 9 or i == 10 or i == 11 or i == 12 or i == 13 or i == 14 or i == 15):
			board[1].append(s4[i])
		if (i == 16 or i == 17 or i == 18 or i == 19 or i == 20 or i == 21 or i == 22 or i == 23):
			board[2].append(s4[i])
		if (i == 24 or i == 25 or i == 26 or i == 27 or i == 28 or i == 29 or i == 30 or i == 31):
			board[3].append(s4[i])
		if (i == 32 or i == 33 or i == 34 or i == 35 or i == 36 or i == 37 or i == 38 or i == 39):
			board[4].append(s4[i])
		if (i == 40 or i == 41 or i == 42 or i == 43 or i == 44 or i == 45 or i == 46 or i == 47):
			board[5].append(s4[i])
		if (i == 48 or i == 49 or i == 50 or i == 51 or i == 52 or i == 53 or i == 54 or i == 55):
			board[6].append(s4[i])
		if (i == 56 or i == 57 or i == 58 or i == 59 or i == 60 or i == 61 or i == 62 or i == 63):
			board[7].append(s4[i])
	
	return board


# Inicializa cliente
connect_client()
