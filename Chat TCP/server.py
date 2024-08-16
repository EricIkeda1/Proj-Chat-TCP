import socket
import threading

# Dados de Conexão
host = '127.0.0.1'  # Endereço IP do servidor (localhost neste caso)
port = 55555        # Porta em que o servidor irá escutar as conexões

# Iniciando o Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de servidor usando IPv4 e TCP
server.bind((host, port))  # Vincula o servidor ao endereço IP e à porta especificados
server.listen()  # Coloca o servidor em modo de escuta para aceitar conexões

# Listas Para Armazenar Clientes e Seus Apelidos
clients = []  # Lista para armazenar os sockets dos clientes conectados
nicknames = []  # Lista para armazenar os apelidos dos clientes conectados

# Enviando Mensagens Para Todos os Clientes Conectados
def broadcast(message):
    for client in clients:  # Itera sobre a lista de clientes conectados
        client.send(message)  # Envia a mensagem para cada cliente

# Tratando Mensagens Recebidas dos Clientes
def handle(client):
    while True:
        try:
            # Recebendo e Broadcast de Mensagens
            message = client.recv(1024)  # Recebe a mensagem do cliente (até 1024 bytes)
            broadcast(message)  # Envia a mensagem para todos os clientes conectados
        except:
            # Removendo e Fechando Conexões de Clientes
            index = clients.index(client)  # Obtém o índice do cliente na lista
            clients.remove(client)  # Remove o cliente da lista
            client.close()  # Fecha a conexão do cliente
            nickname = nicknames[index]  # Obtém o apelido do cliente usando o índice
            broadcast('{} left!'.format(nickname).encode('ascii'))  # Notifica a saída do cliente para os outros
            nicknames.remove(nickname)  # Remove o apelido da lista
            break  # Sai do loop e encerra a função

# Função Para Receber e Escutar Conexões
def receive():
    while True:
        # Aceitar a Conexão
        client, address = server.accept()  # Aceita uma nova conexão e obtém o socket e o endereço do cliente
        print("Connected with {}".format(str(address)))  # Exibe o endereço do cliente conectado

        # Solicitar e Armazenar o Apelido
        client.send('NICK'.encode('ascii'))  # Envia uma mensagem pedindo o apelido do cliente
        nickname = client.recv(1024).decode('ascii')  # Recebe o apelido do cliente
        nicknames.append(nickname)  # Adiciona o apelido à lista de apelidos
        clients.append(client)  # Adiciona o cliente à lista de clientes conectados

        # Exibir e Enviar o Apelido para Todos
        print("Nickname is {}".format(nickname))  # Exibe o apelido no servidor
        broadcast("{} joined!".format(nickname).encode('ascii'))  # Informa a todos que um novo cliente se conectou
        client.send('Connected to server!'.encode('ascii'))  # Confirma a conexão para o cliente

        # Iniciar uma Thread Para Tratar o Cliente
        thread = threading.Thread(target=handle, args=(client,))  # Cria uma nova thread para lidar com o cliente
        thread.start()  # Inicia a thread
        
receive()  # Chama a função para começar a receber conexões
