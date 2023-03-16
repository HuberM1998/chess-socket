# server.py

import socket
import pickle
import numpy as np
import chess


def start_server():
	HOST = "127.0.0.1"
	PORT = 5000
	print("Conectando servidor...")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	if verify_port(PORT,HOST,server) == False:
		print("Porta sendo usada.")
		server.close()
		
	try:
		server.bind((HOST, PORT))
	except:
		print("Erro ao abrir servidor!")
		
	print("Servidor criado!")
	
	# Inicializa o jogo
	ch = chess.Game()
	
	server.listen(2)
	print("Esperando conexão dos jogadores: ")
	conn1, port1 = server.accept()
	print("Player 1 conectado.")
	conn2, port2 = server.accept()
	print("Player 2 conectado.")	
	
	current_turn = conn1
	opponent = conn2	
	
	w1 = 'welcome1'
	current_turn.sendall(pickle.dumps(w1))
	w2 = 'welcome2'
	opponent.sendall(pickle.dumps(w2))
	
	while True:
		fc = current_turn.recv(2048*2)
		from_client1 = pickle.loads(fc)
		
		fc2 = opponent.recv(2048*2)
		from_client2 = pickle.loads(fc2)
		
		if from_client1.startswith('ready') and from_client2.startswith('ready'):
			data1 = 'start' + '\n' + str(ch.board.get_board()) + '\n' + 'True'
			data2 = 'start' + '\n' + str(ch.board.get_board()) + '\n' + 'False'
			current_turn.sendall(pickle.dumps(data1))
			opponent.sendall(pickle.dumps(data2))
		
		elif from_client1.startswith('send move'):
			move = from_client1.split('\n')
			mov = move[1]
			move_from, move_to = ch.transform_input(mov)	
			#if ch.check():
			#	pass
			if ch.move(move_from,move_to):
				current_turn.sendall(pickle.dumps('OK'))
				current_turn, opponent = opponent, current_turn
				update1 = 'update' + '\n' + str(ch.board.get_board()) + '\n' + 'current'
				update2 = 'update' + '\n' + str(ch.board.get_board()) + '\n' + 'opponent'
				current_turn.sendall(pickle.dumps(update1))
				opponent.sendall(pickle.dumps(update2))
			else:
				current_turn.sendall(pickle.dumps('invalid'))
				opponent.sendall(pickle.dumps('wait'))
		
		elif from_client2.startswith('wait'):
			opponent.sendall(pickle.dumps('wait'))
		
		elif from_client1.startswith('give up') or from_client2.startswith('give up'):
			opponent.sendall(pickle.dumps('game end'))
			current_player.sendall(pickle.dumps('game end'))
		
		elif from_client1.startswith('start again') and from_client2.startswith('start again'):
			choice1 = from_client1.split('\n')
			choice2 = from_client2.split('\n')
			if choice1[1] == 'SIM' and choice2[1] == 'SIM':
				ch.reset_board()
				current_turn = conn1
				opponent = conn2
				data1 = 'start' + '\n' + str(ch.board.get_board()) + '\n' + 'True'
				data2 = 'start' + '\n' + str(ch.board.get_board()) + '\n' + 'False'
				current_turn.sendall(pickle.dumps(data1))
				opponent.sendall(pickle.dumps(data2))
			else:
				opponent.sendall(pickle.dumps('end conn'))
				current_player.sendall(pickle.dumps('end conn'))
				print("Servidor será desligado.")
				current_turn.close()
				opponent.close()
		
	current_turn.close()
	opponent.close()

def verify_port(PORT,HOST,sock):
	test = (HOST,PORT)
	result = sock.connect_ex(test)
	if result == 0:
		print("Porta está aberta.")
		return False
	else:
		return True


start_server()
