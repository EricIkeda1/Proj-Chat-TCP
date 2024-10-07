from Crypto.Cipher import DES
import base64
from colorama import init, Fore, Style

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
def rotate_left(bits, n):
    return bits[n:] + bits[:n]

def permute(key, pc_2_table):
    return ''.join([key[i-1] for i in pc_2_table])

def generate_subkey(c1, d1, pc_2_table, shift_amount):
    # Realizar a rotação à esquerda
    c2 = rotate_left(c1, shift_amount)
    d2 = rotate_left(d1, shift_amount)
    
    # Concatenar c2 e d2
    combined = c2 + d2
    
    # Aplicar permutação PC-2
    k2 = permute(combined, pc_2_table)
    return k2

# Dados de entrada
c1 = "11100001100110010101010111111"
d1 = "10101010110011001111100011110"

# Tabela PC-2 fornecida na imagem
pc_2_table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
              26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
              51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

# Número de rotações à esquerda para k2 (2ª iteração)
shift_amount = 1

# Gerar a subchave k2
k2 = generate_subkey(c1, d1, pc_2_table, shift_amount)

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
        if operacao == '1':
            # Gerar a subchave k2
            k2 = generate_subkey(c1, d1, pc_2_table, shift_amount)
            print(f"Subchave k2 gerada: {k2}")
            # Aqui você pode adicionar a lógica de criptografia DES usando a subchave k2
            resultado = "Criptografia DES não implementada."  # Substitua isso pela sua implementação
        else:
            resultado = "Descriptografia DES não implementada."  # Substitua isso pela sua implementação

    return resultado

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