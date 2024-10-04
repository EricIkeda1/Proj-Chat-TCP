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
            resultado = cifra_playfair(texto, chave, 'criptografar')
        else:
            resultado = cifra_playfair(texto, chave, 'descriptografar')

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
        try:
            if len(chave) != 8:
                raise ValueError("A chave deve ter exatamente 8 caracteres.")
            
            cipher = DES.new(chave.encode('utf-8'), DES.MODE_ECB)
            if operacao == '1':  # Criptografar
                # Preencher o texto até um múltiplo de 8 bytes
                while len(texto) % 8 != 0:
                    texto += ' '
                resultado = base64.b64encode(cipher.encrypt(texto.encode('utf-8'))).decode('utf-8')
            else:  # Descriptografar
                decrypted_text = cipher.decrypt(base64.b64decode(texto))
                resultado = decrypted_text.decode('utf-8').strip()  # Remove os espaços preenchidos
        except Exception as e:
            return f"Ocorreu um erro na Cifra DES: {e}"

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