import socket
import threading

# Escolhendo um Nome
nome = input("Escolha seu nome: ")  # Solicita ao usuário que escolha um nome

# Conectando ao Servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de cliente usando IPv4 e TCP
cliente.connect(('127.0.0.1', 55555))  # Conecta o cliente ao servidor usando o endereço IP e a porta especificados

# Função para Ouvir o Servidor e Enviar o Nome
def receber():
    while True:
        try:
            # Recebe a Mensagem do Servidor
            mensagem = cliente.recv(1024).decode('ascii')  # Recebe uma mensagem do servidor (até 1024 bytes) e decodifica para ASCII
            # Se a Mensagem For 'NOME', Envia o Nome
            if mensagem == 'NOME':  # Verifica se a mensagem recebida é uma solicitação de nome
                cliente.send(nome.encode('ascii'))  # Envia o nome do cliente para o servidor
            else:
                print(mensagem)  # Caso contrário, exibe a mensagem recebida no console
        except:
            # Fecha a Conexão em Caso de Erro
            print("Ocorreu um erro!")  # Exibe uma mensagem de erro
            cliente.close()  # Fecha a conexão com o servidor
            break  # Encerra o loop e a função

# Função para Enviar Mensagens ao Servidor
def escrever():
    while True:
        mensagem = '{}: {}'.format(nome, input(''))  # Formata a mensagem incluindo o nome do usuário
        cliente.send(mensagem.encode('ascii'))  # Envia a mensagem para o servidor, codificada em ASCII
        
# Iniciando Threads para Ouvir e Escrever
receber_thread = threading.Thread(target=receber)  # Cria uma nova thread para a função 'receber' (ouvir as mensagens do servidor)
receber_thread.start()  # Inicia a thread de recepção

escrever_thread = threading.Thread(target=escrever)  # Cria uma nova thread para a função 'escrever' (enviar as mensagens ao servidor)
escrever_thread.start()  # Inicia a thread de escrita
