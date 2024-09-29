# Importar a cifra DES
from Crypto.Cipher import DES
import base64

def menu():
    print("===== Programa de Criptografia =====")
    print("Escolha a operação:")
    print("1. Criptografar")
    print("2. Descriptografar")
    operacao = input("Digite o número da operação desejada: ")

    print("\nEscolha a cifra:")
    print("1. Cifra de César")
    print("2. Cifra de Substituição Monoalfabética")
    print("3. Cifra de Playfair")
    print("4. Cifra de Vigenère")
    print("5. Cifra RC4")
    print("6. Cifra DES")
    escolha = input("Digite o número da cifra desejada: ")

    texto = input("\nDigite o texto: ")
    chave = input("Digite a chave: ")

    return operacao, escolha, texto, chave


# Cifra de César
def cifra_cesar(texto, chave, modo='criptografar'):
    resultado = ""
    for char in texto:
        if char.isalpha():
            deslocamento = chave
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            if modo == 'criptografar':
                resultado += chr((ord(char) - base + deslocamento) % 26 + base)
            else:
                resultado += chr((ord(char) - base - deslocamento) % 26 + base)
        else:
            resultado += char
    return resultado

# Cifra de Substituição Monoalfabética
def criar_mapeamento(chave):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chave = chave.upper().replace(' ', '').replace('.', '')  # Remove espaços e pontos da chave
    if len(set(chave)) != 26:  # Verifica se a chave tem 26 caracteres únicos
        raise ValueError("A chave deve ter 26 caracteres únicos.")
    
    mapeamento = {}
    for i in range(len(alfabeto)):
        mapeamento[alfabeto[i]] = chave[i]

    return mapeamento


def substituicao_monoalfabetica(texto, mapeamento):
    resultado = ""

    for letra in texto.upper():
        if letra.isalpha():
            resultado += mapeamento.get(letra, letra)
        else:
            resultado += letra  # Mantém espaços e caracteres não alfabéticos

    return resultado

def inverter_mapeamento(mapeamento):
    return {v: k for k, v in mapeamento.items()}

# Cifra de Playfair
def cria_matriz_playfair(chave):
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    chave = ''.join(dict.fromkeys(chave.upper().replace('J', 'I')))
    matriz = []
    for char in chave:
        if char in alfabeto and char not in matriz:
            matriz.append(char)
    for char in alfabeto:
        if char not in matriz:
            matriz.append(char)
    return matriz

def cifra_playfair(texto, chave, modo='criptografar'):
    matriz = cria_matriz_playfair(chave)
    texto = texto.upper().replace('J', 'I')
    pares = []
    i = 0
    while i < len(texto):
        a = texto[i]
        b = ''
        if (i+1) < len(texto):
            b = texto[i+1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
        else:
            b = 'X'
            i += 1
        pares.append(a + b)

    resultado = ""
    for par in pares:
        a, b = par[0], par[1]
        idx_a = matriz.index(a)
        idx_b = matriz.index(b)
        row_a, col_a = divmod(idx_a, 5)
        row_b, col_b = divmod(idx_b, 5)

        if row_a == row_b:
            if modo == 'criptografar':
                resultado += matriz[row_a * 5 + (col_a + 1) % 5]
                resultado += matriz[row_b * 5 + (col_b + 1) % 5]
            else:
                resultado += matriz[row_a * 5 + (col_a - 1) % 5]
                resultado += matriz[row_b * 5 + (col_b - 1) % 5]
        elif col_a == col_b:
            if modo == 'criptografar':
                resultado += matriz[((row_a + 1) % 5) * 5 + col_a]
                resultado += matriz[((row_b + 1) % 5) * 5 + col_b]
            else:
                resultado += matriz[((row_a - 1) % 5) * 5 + col_a]
                resultado += matriz[((row_b - 1) % 5) * 5 + col_b]
        else:
            resultado += matriz[row_a * 5 + col_b]
            resultado += matriz[row_b * 5 + col_a]
    return resultado

# Cifra de Vigenère
def cifra_vigenere(texto, chave, modo='criptografar'):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    chave = chave.upper()
    resultado = ""
    chave_repetida = ""
    i = 0

    for char in texto:
        if char.isalpha():
            chave_repetida += chave[i % len(chave)]
            i += 1
        else:
            chave_repetida += char

    for idx, char in enumerate(texto):
        if char.isalpha():
            deslocamento = alfabeto.index(chave_repetida[idx])
            if modo == 'criptografar':
                novo_char = alfabeto[(alfabeto.index(char.upper()) + deslocamento) % 26]
            else:
                novo_char = alfabeto[(alfabeto.index(char.upper()) - deslocamento) % 26]
            if char.isupper():
                resultado += novo_char
            else:
                resultado += novo_char.lower()
        else:
            resultado += char
    return resultado

# Cifra RC4
def rc4(key, text):
    # Inicialização do vetor S
    S = list(range(256))
    j = 0
    key_length = len(key)

    # Inicialização da chave
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256  # Convertendo para ASCII
        S[i], S[j] = S[j], S[i]

    # Geração do fluxo de chave e criptografia do texto
    i = j = 0
    result = []
    key_stream = []
    
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))
        key_stream.append(K)  # Armazenar o valor de K

    # Preparação dos resultados para impressão
    encrypted_text = [ord(c) for c in result]
    text_ascii = [ord(c) for c in text]
    key_ascii = [ord(c) for c in key]

    # Impressão dos resultados
    print(f"\tTexto Plano = \"{text}\";")
    print(f"\n\tTexto Plano ASCII = {text_ascii};")
    print(f"\n\tChave= {key}")
    print(f"\n\tChave ASCII = {key_ascii};")
    print(f"\n\tFluxo de chave gerado = {key_stream};")
    print(f"\n\tTexto Cript. = {encrypted_text};")
    print("\n" + "-" * 40 + "\n")
    
    return ''.join(result)

# Cifra de DES
def cifra_des(texto, chave, modo='criptografar'):
    chave = chave.encode('utf-8')
    if len(chave) < 8:
        chave = chave.ljust(8, b' ')
    else:
        chave = chave[:8]

    cipher = DES.new(chave, DES.MODE_ECB)
    padding = 8 - (len(texto) % 8)
    texto_padded = texto + (chr(padding) * padding)
    if modo == 'criptografar':
        criptografado = cipher.encrypt(texto_padded.encode('utf-8'))
        return base64.b64encode(criptografado).decode('utf-8')
    else:
        decodificado = base64.b64decode(texto)
        descriptografado = cipher.decrypt(decodificado).decode('utf-8')
        pad = ord(descriptografado[-1])
        return descriptografado[:-pad]

# Processamento da Escolha do Usuário
# Processamento da Escolha do Usuário
def processar_operacao(operacao, escolha, texto, chave):
    if escolha == '1':  # Cifra de César
        try:
            chave_num = int(chave)
        except ValueError:
            return "Chave inválida para a Cifra de César. Deve ser um número inteiro."
        if operacao == '1':
            resultado = cifra_cesar(texto, chave_num, 'criptografar')
        else:
            resultado = cifra_cesar(texto, chave_num, 'descriptografar')
    elif escolha == '2':  # Cifra de Substituição Monoalfabética
        mapeamento = criar_mapeamento(chave)
        if operacao == '1':
            resultado = substituicao_monoalfabetica(texto, mapeamento)
        else:
            mapeamento_invertido = inverter_mapeamento(mapeamento)
            resultado = substituicao_monoalfabetica(texto, mapeamento_invertido)
    elif escolha == '3':  # Cifra de Playfair
        if operacao == '1':
            resultado = cifra_playfair(texto, chave, 'criptografar')
        else:
            resultado = cifra_playfair(texto, chave, 'descriptografar')
    elif escolha == '4':  # Cifra de Vigenère
        if operacao == '1':
            resultado = cifra_vigenere(texto, chave, 'criptografar')
        else:
            resultado = cifra_vigenere(texto, chave, 'descriptografar')
    elif escolha == '5':  # Cifra RC4
        resultado = rc4(chave, texto)  # Corrigido para chamar rc4 com 2 argumentos
    elif escolha == '6':  # Cifra DES
        if operacao == '1':
            resultado = cifra_des(texto, chave, 'criptografar')
        else:
            resultado = cifra_des(texto, chave, 'descriptografar')
    else:
        resultado = "Escolha inválida."
    return resultado

# Executa o programa
operacao, escolha, texto, chave = menu()
resultado = processar_operacao(operacao, escolha, texto, chave)
print(f"\nResultado:\n{resultado}")
