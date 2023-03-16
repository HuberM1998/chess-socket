import socket
import threading

HOST = '127.0.0.1'
PORT = 6000

def receive_messages():
    while True:
        data = client.recv(1024).decode()
        print(f"Outro jogador: {data}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    message = input("Sua mensagem: ")
    client.sendall(message.encode())
