import socket
from getpass import getpass
from rich.console import Console

console = Console()
console.print('Iniciando o cliente...', style='green')

key = "fogo"
server_address = ('localhost', 3000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)
console.print('Conectado ao servidor.', style='green')

def criar_matriz_playfair(chave):
    alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I e J combinados
    matriz = []
    used = {}

    # Adiciona a chave à matriz, removendo duplicatas
    for char in chave.upper():
        if char not in used and char != ' ':
            matriz.append(char)
            used[char] = True

    # Adiciona as letras restantes do alfabeto à matriz
    for char in alfabeto:
        if char not in used:
            matriz.append(char)

    # Forma a matriz 5x5
    return [matriz[i:i + 5] for i in range(0, 25, 5)]

def encontrar_indices(matriz, letra):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == letra.upper():
                return (i, j)
    return (-1, -1)  # Letra não encontrada

def criptografar_playfair(texto, chave):
    matriz = criar_matriz_playfair(chave)
    texto_cifrado = ''
    digrama = ''
    texto_sem_espacos = texto.replace(' ', '')  # Remove espaços temporariamente

    # Adiciona um caractere de preenchimento se o comprimento do texto for ímpar
    if len(texto_sem_espacos) % 2 != 0:
        texto_sem_espacos += 'X'  # 'X' é um caractere de preenchimento comum

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

            if i1 == i2:  # Mesma linha
                texto_cifrado += matriz[i1][(j1 + 1) % 5] + matriz[i2][(j2 + 1) % 5]
            elif j1 == j2:  # Mesma coluna
                texto_cifrado += matriz[(i1 + 1) % 5][j1] + matriz[(i2 + 1) % 5][j2]
            else:  # Diferentes linha e coluna
                texto_cifrado += matriz[i1][j2] + matriz[i2][j1]
            digrama = ''

    # Adiciona espaços de volta no texto cifrado
    texto_com_espacos = ''
    indice_texto_cifrado = 0

    for i in range(len(texto)):
        if texto[i] == ' ':
            texto_com_espacos += ' '
        else:
            texto_com_espacos += texto_cifrado[indice_texto_cifrado]
            indice_texto_cifrado += 1

    return texto_com_espacos

def descriptografar_playfair(texto_cifrado, chave):
    matriz = criar_matriz_playfair(chave)
    texto_claro = ''
    digrama = ''
    texto_sem_espacos = texto_cifrado.replace(' ', '')  # Remove espaços temporariamente

    # Adiciona um caractere de preenchimento se o comprimento do texto cifrado for ímpar
    if len(texto_sem_espacos) % 2 != 0:
        texto_sem_espacos += 'X'  # 'X' é um caractere de preenchimento comum

    for i in range(0, len(texto_sem_espacos), 2):
        char1 = texto_sem_espacos[i].upper()
        char2 = texto_sem_espacos[i + 1].upper()

        # Verifica se os caracteres são válidos
        if not (char1.isalpha() and char2.isalpha()):
            console.print("Caractere inválido no texto cifrado.", style='red')
            return

        i1, j1 = encontrar_indices(matriz, char1)
        i2, j2 = encontrar_indices(matriz, char2)

        if i1 == i2:
            texto_claro += matriz[i1][(j1 - 1 + 5) % 5] + matriz[i2][(j2 - 1 + 5) % 5]
        elif j1 == j2:
            texto_claro += matriz[(i1 - 1 + 5) % 5][j1] + matriz[(i2 - 1 + 5) % 5][j2]
        else:
            texto_claro += matriz[i1][j2] + matriz[i2][j1]

    # Remove o caractere de preenchimento se estiver no final do texto claro
    if texto_claro.endswith('X'):
        texto_claro = texto_claro[:-1]

    # Adiciona espaços de volta no texto claro
    texto_com_espacos = ''
    indice_texto_claro = 0

    for i in range(len(texto_cifrado)):
        if texto_cifrado[i] == ' ':
            texto_com_espacos += ' '
        else:
            if indice_texto_claro < len(texto_claro):
                texto_com_espacos += texto_claro[indice_texto_claro]
                indice_texto_claro += 1

    return texto_com_espacos

# Loop principal para interagir com o usuário
try:
    while True:
        msg = input('Mensagem: ')
        chave = getpass('Chave: ')
        x = criptografar_playfair(msg, chave)
        console.print(f'Mensagem criptografada: {x}', style='blue')
        y = descriptografar_playfair(x, chave)
        console.print(f'Texto plano: {y}', style='blue')
        client.sendall(x.encode('utf-8'))
except Exception as e:
    console.print(f'Erro: {str(e)}', style='red')
finally:
    client.close()
    console.print('Desconectado do servidor.', style='red')
