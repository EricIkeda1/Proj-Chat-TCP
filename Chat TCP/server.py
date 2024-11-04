import socket
import threading

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''
    deslocamento = chave if criptografar else -chave
    for caractere in mensagem:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere
    return resultado

# Função que gerencia as mensagens recebidas dos clientes
def gerenciar_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            if not mensagem:
                break
            operacao, escolha, texto, chave = mensagem.split(',')

            # Realiza a operação correspondente
            if escolha == '1':  # Cifra de César
                chave_int = int(chave)
                if operacao == '1':  # Criptografar
                    resultado = cifra_de_cesar(texto, chave_int, True)
                else:  # Descriptografar
                    resultado = cifra_de_cesar(texto, chave_int, False)
            else:
                resultado = "Cifra não suportada ainda."

            cliente.send(resultado.encode('ascii'))
        except:
            break

    cliente.close()

# Função que recebe novas conexões de clientes
def aceitar_conexoes(servidor):
    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado com {str(endereco)}")
        threading.Thread(target=gerenciar_cliente, args=(cliente,)).start()

# Função para iniciar o servidor
def abrir_servidor():
    bind_ip = '0.0.0.0'
    bind_port = 50000
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((bind_ip, bind_port))
    servidor.listen()
    print(f"Servidor iniciado e ouvindo na porta {bind_port}")
    return servidor

if __name__ == "__main__":
    servidor = abrir_servidor()
    aceitar_conexoes(servidor)
