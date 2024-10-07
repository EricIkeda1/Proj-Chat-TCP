from Crypto.Cipher import DES
import base64
from colorama import init, Fore, Style
from numpy import left_shift

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

    # Se a escolha for DES e a operação for de descriptografia, não solicita entrada de texto e chave
    if escolha == '6' and operacao == '2':
        texto = input("\nDigite o texto criptografado: ")
        chave = input("Digite a chave (8 caracteres): ")
    else:
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
def criar_matriz_playfair(chave):
    alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    matriz = []
    usado = {}

    for char in chave.upper():
        if char not in usado and char != ' ':
            matriz.append(char)
            usado[char] = True

    for char in alfabeto:
        if char not in usado:
            matriz.append(char)

    return [matriz[i:i + 5] for i in range(0, len(matriz), 5)]

def encontrar_indices(matriz, letra):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == letra.upper():
                return (i, j)
    return (-1, -1)

def criptografar_playfair(texto, chave):
    matriz = criar_matriz_playfair(chave)
    texto_cifrado = ''
    digrama = ''
    texto_sem_espacos = texto.replace(' ', '')

    if len(texto_sem_espacos) % 2 != 0:
        texto_sem_espacos += 'X'  # Caractere de preenchimento

    for i in range(len(texto_sem_espacos)):
        char = texto_sem_espacos[i]
        char_upper = char.upper()
        if char_upper == 'J':
            digrama += 'I'
        else:
            digrama += char_upper

        if len(digrama) == 2:
            i1, j1 = encontrar_indices(matriz, digrama[0])
            i2, j2 = encontrar_indices(matriz, digrama[1])

            if i1 == i2:
                texto_cifrado += matriz[i1][(j1 + 1) % 5] + matriz[i2][(j2 + 1) % 5]
            elif j1 == j2:
                texto_cifrado += matriz[(i1 + 1) % 5][j1] + matriz[(i2 + 1) % 5][j2]
            else:
                texto_cifrado += matriz[i1][j2] + matriz[i2][j1]
            digrama = ''

    return texto_cifrado

def descriptografar_playfair(texto_cifrado, chave):
    matriz = criar_matriz_playfair(chave)
    texto_claro = ''
    texto_sem_espacos = texto_cifrado.replace(' ', '')

    if len(texto_sem_espacos) % 2 != 0:
        print(Fore.RED + "Texto cifrado tem comprimento ímpar.")
        return

    for i in range(0, len(texto_sem_espacos), 2):
        char1 = texto_sem_espacos[i].upper()
        char2 = texto_sem_espacos[i + 1].upper()

        if not char1.isalpha() or not char2.isalpha():
            print(Fore.RED + "Caractere inválido no texto cifrado.")
            return

        i1, j1 = encontrar_indices(matriz, char1)
        i2, j2 = encontrar_indices(matriz, char2)

        if i1 == i2:
            texto_claro += matriz[i1][(j1 - 1) % 5] + matriz[i2][(j2 - 1) % 5]
        elif j1 == j2:
            texto_claro += matriz[(i1 - 1) % 5][j1] + matriz[(i2 - 1) % 5][j2]
        else:
            texto_claro += matriz[i1][j2] + matriz[i2][j1]

    texto_claro = texto_claro.replace('X', '')  # Remove 'X' no final, se necessário

    return texto_claro

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
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

SBOX = [
    # S-box 1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    # S-box 2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    # S-box 3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 2, 8, 4, 7, 12, 11],
     [7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 0, 15, 3, 8],
     [5, 1, 2, 14, 9, 10, 0, 6, 12, 11, 4, 7, 13, 15, 8, 3],
     [2, 14, 12, 4, 1, 7, 10, 11, 6, 8, 0, 13, 3, 5, 9, 15]],

    # S-box 4
    [[3, 15, 0, 6, 10, 1, 13, 7, 4, 9, 2, 8, 5, 11, 14, 12],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 9, 11, 12, 0, 6, 3, 5],
     [8, 13, 3, 15, 4, 7, 5, 10, 1, 2, 14, 12, 0, 9, 11, 6]],

    # S-box 5
    [[2, 12, 4, 1, 7, 10, 11, 6, 9, 0, 5, 14, 15, 13, 3, 8],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 4, 2, 13, 0, 6, 9, 10, 14, 3, 5, 15],
     [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 4, 5, 3, 11, 14, 7]],

    # S-box 6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 4, 5, 3, 11, 14, 7],
     [4, 11, 2, 14, 15, 0, 8, 13, 3, 6, 12, 9, 5, 10, 7, 1],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     [7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 0, 15, 3, 8]],

    # S-box 7
    [[2, 12, 4, 1, 7, 10, 11, 6, 9, 0, 5, 14, 15, 13, 3, 8],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 4, 2, 13, 0, 6, 9, 10, 14, 3, 5, 15],
     [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 4, 5, 3, 11, 14, 7]],

    # S-box 8
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 4, 5, 3, 11, 14, 7],
     [4, 11, 2, 14, 15, 0, 8, 13, 3, 6, 12, 9, 5, 10, 7, 1],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     [7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 0, 15, 3, 8]],
]

# Tabelas para geração de chaves (PC1, PC2, shifts)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

shifts = [1, 1, 2, 2, 2, 2, 2, 2,
          1, 2, 2, 2, 2, 2, 2, 1]

def text_to_hex(texto):
    """Converte texto em uma representação hexadecimal."""
    return ' '.join(format(ord(c), '02X') for c in texto)

def hex_to_bin(chave):
    """Converte chave hexadecimal em uma representação binária."""
    return ''.join(format(int(c, 16), '04b') for c in chave.split())

def xor(a, b):
    """Realiza a operação XOR entre duas strings binárias."""
    if len(a) != len(b):
        raise ValueError("As strings devem ter o mesmo comprimento para a operação XOR.")
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def permute(block, table):
    """Aplica uma permutação em um bloco baseado em uma tabela de permutação."""
    return ''.join(block[i - 1] for i in table)

def f(R, K):
    """Função de Feistel, aplica expansão e XOR com a chave, depois permuta."""
    # Implementar a lógica da função F conforme a cifra DES
    return R

def des(texto, chave):
    """Implementa a criptografia DES."""
    # Lógica do DES: deve incluir a geração de chaves e os rounds de criptografia
    # Para simplificação, o código aqui é uma representação
    resultado = ''
    for i in range(0, len(texto), 64):
        block = texto[i:i + 64]
        # Simule o processo DES
        L, R = block[:32], block[32:]
        # Adicione a lógica de rounds e aplique a chave corretamente
        resultado += L + R  # Placeholder: Retorna o bloco sem alteração
    return resultado  # Retorne o resultado da criptografia

# Gerar chaves para DES
def generate_keys(key):
    key = permute(key, PC1)
    
    # Gerar 16 subchaves
    subkeys = []
    L, R = key[:28], key[28:]
    
    for i in range(16):
        L = left_shift(L, shifts[i])
        R = left_shift(R, shifts[i])
        subkeys.append(permute(L + R, PC2))
    
    return subkeys

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
            resultado = criptografar_playfair(texto, chave)  # Removido 'criptografar'
        else:
            resultado = descriptografar_playfair(texto, chave) 

    elif escolha == '4':  # Cifra de Vigenère
        if operacao == '1':
            resultado = cifra_vigenere(texto, chave, 'criptografar')
        else:
            resultado = cifra_vigenere(texto, chave, 'descriptografar')

    elif escolha == '5':  # Cifra RC4
        if operacao == '1':  # Criptografar
            resultado = rc4(chave, texto)
        else:  # Descriptografar
            try:
                # Converte a string da lista para uma lista de inteiros
                encrypted_text = eval(texto)  # Avalia a string para uma lista
                # Descriptografar, utilizando os valores ASCII convertidos
                original_text = ''.join(chr(c) for c in rc4(chave, ''.join(chr(c) for c in encrypted_text)))
                resultado = original_text
            except Exception as e:
                resultado = f"Erro na descriptografia: {e}"

    elif escolha == '6':  # Cifra DES
        if operacao == '1':  # Cifra DES
            hex_texto = text_to_hex(texto)  # Converte o texto para hexadecimal
            print(f"Texto Plano: {texto}")
            print(f"Chave: {chave} (HEXADECIMAL)")
            print(f"Converter para texto plano e chave para hexadecimal.")
            print(f"Texto Plano = {hex_texto}")

        # Converter texto em binário
            bin_texto = ''.join(format(int(c, 16), '04b') for c in hex_texto.split())
        
        # Separar em blocos de 64 bits
            print("Separar em blocos de 64 bits.")
            bin_texto = bin_texto.replace(" ", "")  # Remove os espaços
            while len(bin_texto) % 64 != 0:  # Adiciona padding se necessário
                bin_texto += '0'
        
        # Divide o texto binário em blocos de 64 bits
            blocos = [bin_texto[i:i + 64] for i in range(0, len(bin_texto), 64)]
            print(f"Texto Plano = {' '.join(hex_texto.split())}")

        # Criptografar cada bloco
            resultado = ''
            for bloco in blocos:
                resultado += des(bloco, hex_to_bin(chave))  # Chama a função de criptografia DES

            return resultado 
        
        # Exibindo informações
        print(f"Texto Plano: {hex_texto}")
        print(f"Chave: {chave} (HEXADECIMAL)")
        
        # Separar em blocos de 64 bits
        print(f"Texto Plano em HEX: {hex_texto} (depois da conversão)")
        bin_texto = bin_texto.replace(" ", "")  # Remove os espaços
        while len(bin_texto) % 64 != 0:  # Adiciona padding se necessário
            bin_texto += '0'
        
        print(f"Texto Plano em binário (com padding se necessário): {bin_texto}")

# Execução do programa
def main():
    while True:
        operacao, escolha, texto, chave = menu()
        resultado = processar_operacao(operacao, escolha, texto, chave)
        print(f"Resultado: {resultado}")
        continuar = input("Deseja continuar? (s/n): ")
        if continuar.lower() != 's':
            break

if __name__ == "__main__":
    main()