import socket
import threading

# Escolhendo um Apelido
nickname = input("Choose your nickname: ")  # Solicita ao usuário que escolha um apelido

# Conectando ao Servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de cliente usando IPv4 e TCP
client.connect(('127.0.0.1', 55555))  # Conecta o cliente ao servidor usando o endereço IP e a porta especificados

# Função para Ouvir o Servidor e Enviar o Apelido
def receive():
    while True:
        try:
            # Recebe a Mensagem do Servidor
            message = client.recv(1024).decode('ascii')  # Recebe uma mensagem do servidor (até 1024 bytes) e decodifica para ASCII
            # Se a Mensagem For 'NICK', Envia o Apelido
            if message == 'NICK':  # Verifica se a mensagem recebida é uma solicitação de apelido
                client.send(nickname.encode('ascii'))  # Envia o apelido do cliente para o servidor
            else:
                print(message)  # Caso contrário, exibe a mensagem recebida no console
        except:
            # Fecha a Conexão em Caso de Erro
            print("An error occured!")  # Exibe uma mensagem de erro
            client.close()  # Fecha a conexão com o servidor
            break  # Encerra o loop e a função

# Função para Enviar Mensagens ao Servidor
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))  # Formata a mensagem incluindo o apelido do usuário
        client.send(message.encode('ascii'))  # Envia a mensagem para o servidor, codificada em ASCII
        
# Iniciando Threads para Ouvir e Escrever
receive_thread = threading.Thread(target=receive)  # Cria uma nova thread para a função 'receive' (ouvir as mensagens do servidor)
receive_thread.start()  # Inicia a thread de recepção

write_thread = threading.Thread(target=write)  # Cria uma nova thread para a função 'write' (enviar as mensagens ao servidor)
write_thread.start()  # Inicia a thread de escrita
