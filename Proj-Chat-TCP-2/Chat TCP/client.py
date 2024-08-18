import socket
import threading

print("Tarefa 2")

print("Atividade em Dupla: Implementação de Cifras Clássicas em um Chat TCP")

# Conectando ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Solicitar ao usuário que digite o número do servidor e a porta
server_ip = input("Digite o endereço IP do servidor exemplo '127.0.0.1': ")
server_port = input("Digite a porta do servidor, exemplo '55555': ")

# Conectar ao servidor usando os valores fornecidos pelo usuário
client.connect((server_ip, int(server_port)))

# Escolhendo um apelido
nickname = input("Escolha seu apelido:\n ")


print("1.Cifra de César")
print("2.Substituição Monoalfabética")
print("3.Cifra de Playfair")
print("4.Cifra de Vigenère")
        
# Usuário vai digitar e ser lido uma das opções
cifra = input("Digite uma das opções, cifra de criptografia a ser utilizada: \n") 
        

#Em seguida, o usuário deverá fornecer a chave previamente combinada com seu parceiro.
chave = input("Digite o valor da chave entre 1 a 4, para codificar e decodificar a mensagem: \n") 


# Agora o cliente está conectado ao servidor usando os valores digitados pelo usuário
# Função para ouvir o servidor e enviar o apelido
def receive():
    while True:
        try:
            # Receber mensagem do servidor
            # Se a mensagem for 'NICK', enviar o apelido
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Fechar conexão em caso de erro
            print("Ocorreu um erro!")
            client.close()
            break
        
# Função para enviar mensagens ao servidor
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))
        
# Iniciando threads para ouvir e escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
