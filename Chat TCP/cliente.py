import socket
import threading

# Escolha da cifra de criptografia pelo usuário
print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")
print("5. RC4")
print("6. DES")
escolha = input("Digite o número da cifra desejada: ")

# Solicitação da chave de criptografia
chave = input("Digite a chave previamente combinada com seu parceiro: ")

# Solicitação do texto plano apenas se RC4 for selecionada
texto_plano = ""
if escolha == '5' or escolha == '6':
    texto_plano = input("Digite o texto plano: ")

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

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Alfabeto original
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'  # Alfabeto substituído
    
    chave = chave.upper()  # Converte a chave para maiúsculas
    
    if criptografar:
        # Cria um mapa de substituição usando o alfabeto original e substituído
        mapa_chave = {alfabeto[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        # Cria um mapa de substituição invertido para descriptografar
        mapa_chave = {alfabeto_substituido[i]: alfabeto[i] for i in range(26)}

    resultado = ''  # Inicializa a string para armazenar o resultado
    for caractere in mensagem.upper():  # Converte a mensagem para maiúsculas e itera sobre cada caractere
        resultado += mapa_chave.get(caractere, caractere)  # Substitui o caractere ou mantém o original
    return resultado  # Retorna a mensagem criptografada ou descriptografada


# Função que implementa a Cifra de Playfair
class Playfair:
    def __init__(self, key):
        self.enc = {}
        self.dec = {}
        self.create_key_matrix(key)

    def uniq(self, seq):
        seen = []
        for x in seq:
            if x not in seen:
                seen.append(x)
        return seen

    def partition(self, seq, n):
        return [seq[i:i + n] for i in range(0, len(seq), n)]

    def canonicalize(self, s):
        return s.upper().replace('J', 'I').replace(' ', '')

    def create_key_matrix(self, key):
        # Concatena a chave com o alfabeto completo, remove duplicatas
        key = self.canonicalize(key + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        matrix = self.partition(self.uniq(key), 5)

        # Exibe a matriz para depuração
        print("Matriz de chaves:")
        for row in matrix:
            print(row)

        # Mapeia as letras para seus pares cifrados (linhas e colunas)
        for row in range(5):
            for col in range(5):
                for i in range(5):
                    if col != i:
                        self.enc[matrix[row][col] + matrix[row][i]] = matrix[row][(i + 1) % 5] + matrix[row][(col + 1) % 5]
                        self.dec[matrix[row][(i + 1) % 5] + matrix[row][(col + 1) % 5]] = matrix[row][col] + matrix[row][i]

        # Adiciona substituições de pares diagonais
        for i1 in range(5):
            for j1 in range(5):
                for i2 in range(5):
                    for j2 in range(5):
                        if i1 != i2 and j1 != j2:
                            self.enc[matrix[i1][j1] + matrix[i2][j2]] = matrix[i1][j2] + matrix[i2][j1]
                            self.dec[matrix[i1][j2] + matrix[i2][j1]] = matrix[i1][j1] + matrix[i2][j2]

    def encode(self, text):
        text = self.canonicalize(text)
        lst = []
        i = 0
        while i < len(text) - 1:
            if text[i] == text[i + 1]:
                lst.append(text[i] + 'X')
                i += 1
            else:
                lst.append(text[i:i + 2])
                i += 2
        if i == len(text) - 1:
            lst.append(text[i] + 'X')  # Adiciona X ao final se o número de caracteres for ímpar
        
        # Retorna o texto cifrado
        return ' '.join(self.enc.get(pair, pair) for pair in lst)

    def decode(self, text):
        pairs = self.partition(text.replace(' ', ''), 2)
        return ''.join(self.dec.get(pair, pair) for pair in pairs)

# Função que implementa a Cifra de Vigenère
def cifra_de_vigenere(mensagem, chave, criptografar=True):
    resultado = ''
    chave = chave.lower()
    indice_chave = 0
    
    for caractere in mensagem:
        if caractere.isalpha():
            deslocamento = ord(chave[indice_chave]) - ord('a')
            deslocamento = deslocamento if criptografar else -deslocamento
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
            indice_chave = (indice_chave + 1) % len(chave)
        else:
            resultado += caractere
    return resultado

texto_plano = "ATACARBASENORTE"
chave = "FOGO"
texto_criptografado = cifra_de_vigenere(texto_plano, chave)
print("Texto cifrado:", texto_criptografado)
    
# Função RC4
def rc4(key, text):
    S = list(range(256))
    j = 0
    key_length = len(key)
    
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))
    
    return ''.join(result)

# Função que implementa o DES
def executar_des():
    # Seu código do DES já implementado
    c1 = [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1]
    d1 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    ls_array = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    def shift_left(arr, n):
        return arr[n:] + arr[:n]

    c1s = c1[:]
    d1s = d1[:]

    for i in range(16):
        iteration_count = ls_array[i]
        c1s = shift_left(c1s, iteration_count)
        d1s = shift_left(d1s, iteration_count)

    def permute_pc2(c, d, pc2):
        combined = c + d
        permuted_key = [combined[index - 1] for index in pc2]
        return permuted_key

    key = permute_pc2(c1s, d1s, pc2)

    print("Chave calculada:", key)
    print("Comprimento da chave:", len(key))
    return key

# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem, escolha, chave):
    if escolha == '5':  # RC4
        chave_bytes = chave  # Para RC4, a chave deve ser uma string de bytes
        return rc4(chave_bytes, mensagem)
    else:
        # Outras cifras podem ser implementadas aqui
        return mensagem

# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem, escolha, chave):
    if escolha == '1':
        return cifra_de_cesar(mensagem, int(chave))
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)
    elif escolha == '3':
        playfair = Playfair(chave)
        return playfair.encode(mensagem)
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)
    elif escolha == '6':  # DES
        print("Executando DES...")
        key = executar_des()
        print(f"Texto Criptografado com DES: {mensagem}") 
        return mensagem  
    else:
        return mensagem

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            if escolha == '3':
                texto_plano = input("Digite o texto plano (para Cifra de Playfair): ")
                print(f"Texto Plano: {texto_plano}")
            if escolha == '5':  # RC4
                print(f"Texto Plano: {texto_plano}")
                texto_plano_ascii = [ord(c) for c in texto_plano]
                print(f"Texto Plano ASCII: {texto_plano_ascii}")
                mensagem_criptografada = criptografar_mensagem(texto_plano, escolha, chave)
                print(f"Texto Criptografado: {[ord(c) for c in mensagem_criptografada]}")
                print(f"Chave: {chave}")
                chave_ascii = [ord(c) for c in chave]
                print(f"Chave ASCII: {chave_ascii}")
            else:
                print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break
        
# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))
        mensagem_criptografada = criptografar_mensagem(mensagem, escolha, chave)
        if escolha == '5':  # RC4
            print(f"Texto Criptografado a ser enviado: {[ord(c) for c in mensagem_criptografada]}")
        cliente.send(''.join(mensagem_criptografada).encode('ascii'))
        
def conectar():
    global cliente
    target_host = input("Digite o IP do servidor ao qual deseja se conectar: ")
    target_port = 50000  # Porta padrão
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((target_host, target_port))
    print(f"Conectado ao servidor {target_host} na porta {target_port}")
    print("Aperte Enter para Prosseguir")
    print("Digite a mensagem:")
    
def main():
    conectar()
    while True:
        global comandos
        comandos = cliente.recv(4000).decode()
            
# Iniciando o cliente
apelido = input("Escolha um apelido: ")
conectar()

# Iniciando threads para envio e recebimento de mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
