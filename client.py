# client.py 

import socket
import pickle
import threading
import numpy as np

HOST = "127.0.0.1"
PORT = 5000


class Client():

	def connect_client():
		try:	
			client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Conectando cliente ao servidor ...")
			client.connect((HOST, PORT))
			print("Conectado ao servidor!")
			thread.start_new_thread(recv_menssage, (client, ))
		except: 
			print("1:ERROR! Conexão ao servidor não foi um sucesso!")			
	
	def recv_message(client):
		global turn, winner
		turn = 'True'
		
		client.send('ready'.encode())
		
		while True:
			from_server = str(client.recv(2048).decode())
			
			if not from_server:
				break
			
			if from_server.startswith("welcome"):
				if from_server == "welcome1":
					print("Bem vindo jogador 1")
					print("|              Xadrez                   |")
					print("| Peças brancas são em letra maiuscula. |")
					print("| Peças pretas são em letra minuscula.  |")
				elif from_server == "welcome2":
					print("Bem vindo jogador 2")
					print("|              Xadrez                   |")
					print("| Peças brancas são em letra maiuscula. |")
					print("| Peças pretas são em letra minuscula.  |")
			
			elif from_server.startswith("start"):
				print("Jogo vai começar.")
				game_begin = from_server.split('\n')
				print_state(game_begin[1])
				if game_begin[2] == turn:
					send_move(client,game_begin[2])
					turn = 'False'
				
			elif from_server.startswith("update"):
				board = from_serer.split('\n')
				print_state(board[1])
				if board[2] == turn:
					send_move(client,board[2])
				elif board[2] != turn:
					print("Esperando jogador adversário.")
					
			elif from_server.startswith("end game"):
				pass
			elif from_server.startswith("p_dis"):
				pass
			elif from_server.startswith("end conn"):
				pass
				
		client.close()
	
	def send_move(client,isTurn):
		move = input("Faça seu movimento (ex. e2 e4): ")
		while len(list(move)) != 5:
			print(f'7: Formato de entrada incorreto. Formato: e2 e4')
		
		mm = 'send move' + '\n' + move  
        	client.send(mm.encode())
		
		if isTurn == 'True':
			turn = 'False'
		elif isTurn == 'False'
			turn = 'True'
	
	def disconnect(client):
		client.close()
	
	# Imprime o estado atual do jogo
	def print_state(state):
		line = [' ','a','b','c','d','e','f','g','h']
		column = [['8'],['7'],['6'],['5'],['4'],['3'],['2'],['1']]
		bP= np.hstack((column,state))
		for row in bP:
			print(' '.join(row))
		for i in line:
			print(i, end = ' ')
		print(f'\n')

# Inicializa cliente
client = Client()
client.connect_client()
