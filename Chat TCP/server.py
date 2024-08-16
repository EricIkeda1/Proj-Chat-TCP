import socket
import threading

# Dados de Conexão
host = '127.0.0.1'  # Endereço IP do servidor (localhost neste caso)
port = 55555        # Porta em que o servidor irá escutar as conexões

# Iniciando o Servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de servidor usando IPv4 e TCP
servidor.bind((host, port))  # Vincula o servidor ao endereço IP e à porta especificados
servidor.listen()  # Coloca o servidor em modo de escuta para aceitar conexões

# Listas Para Armazenar Clientes e Seus Nomes
clientes = []  # Lista para armazenar os sockets dos clientes conectados
nomes = []  # Lista para armazenar os nomes dos clientes conectados

# Enviando Mensagens Para Todos os Clientes Conectados
def transmitir(mensagem):
    for cliente in clientes:  # Itera sobre a lista de clientes conectados
        cliente.send(mensagem)  # Envia a mensagem para cada cliente

# Tratando Mensagens Recebidas dos Clientes
def lidar(cliente):
    while True:
        try:
            # Recebendo e Transmitindo Mensagens
            mensagem = cliente.recv(1024)  # Recebe a mensagem do cliente (até 1024 bytes)
            transmitir(mensagem)  # Envia a mensagem para todos os clientes conectados
        except:
            # Removendo e Fechando Conexões de Clientes
            indice = clientes.index(cliente)  # Obtém o índice do cliente na lista
            clientes.remove(cliente)  # Remove o cliente da lista
            cliente.close()  # Fecha a conexão do cliente
            nome = nomes[indice]  # Obtém o nome do cliente usando o índice
            transmitir('{} saiu!'.format(nome).encode('ascii'))  # Notifica a saída do cliente para os outros
            nomes.remove(nome)  # Remove o nome da lista
            break  # Sai do loop e encerra a função

# Função Para Receber e Escutar Conexões
def receber():
    while True:
        # Aceitar a Conexão
        cliente, endereco = servidor.accept()  # Aceita uma nova conexão e obtém o socket e o endereço do cliente
        print("Conectado com {}".format(str(endereco)))  # Exibe o endereço do cliente conectado

        # Solicitar e Armazenar o Nome
        cliente.send('NOME'.encode('ascii'))  # Envia uma mensagem pedindo o nome do cliente
        nome = cliente.recv(1024).decode('ascii')  # Recebe o nome do cliente
        nomes.append(nome)  # Adiciona o nome à lista de nomes
        clientes.append(cliente)  # Adiciona o cliente à lista de clientes conectados

        # Exibir e Enviar o Nome para Todos
        print("O nome é {}".format(nome))  # Exibe o nome no servidor
        transmitir("{} entrou!".format(nome).encode('ascii'))  # Informa a todos que um novo cliente se conectou
        cliente.send('Conectado ao servidor!'.encode('ascii'))  # Confirma a conexão para o cliente

        # Iniciar uma Thread Para Tratar o Cliente
        thread = threading.Thread(target=lidar, args=(cliente,))  # Cria uma nova thread para lidar com o cliente
        thread.start()  # Inicia a thread
        
receber()  # Chama a função para começar a receber conexões
