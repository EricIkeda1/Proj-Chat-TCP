import socket
import threading

# Dados da conexão
host = '127.0.0.1'
port = 55555

# Iniciando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas para clientes e seus apelidos
clients = []
nicknames = []

# Função para enviar mensagens para todos os clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)
        
# Função para lidar com mensagens dos clientes
def handle(client):
    while True:
        try:
            # Recebendo mensagens e transmitindo para todos os clientes
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removendo e fechando clientes desconectados
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
        
# Função para receber conexões
def receive():
    while True:
        # Aceitando conexão
        client, address = server.accept()
        print("Conectado com {}".format(str(address)))

        # Solicitando e armazenando apelido
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Imprimindo e transmitindo apelido
        print("Apelido é {}".format(nickname))
        broadcast("{} entrou!".format(nickname).encode('ascii'))
        client.send('Conectado ao servidor, Opções!'.encode('ascii'))


        # Iniciando thread para lidar com o cliente
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
receive()
