import socket

HOST = '127.0.0.1'
PORT = 6000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor está ouvindo na porta {PORT}")

conn1, addr1 = server.accept()
print(f"Jogador 1 conectado com {addr1}")

conn2, addr2 = server.accept()
print(f"Jogador 2 conectado com {addr2}")

while True:
    data = conn1.recv(1024).decode()
    if not data:
        break
    print(f"Jogador 1: {data}")
    conn2.sendall(data.encode())

    data = conn2.recv(1024).decode()
    if not data:
        break
    print(f"Jogador 2: {data}")
    conn1.sendall(data.encode())

conn1.close()
conn2.close()
