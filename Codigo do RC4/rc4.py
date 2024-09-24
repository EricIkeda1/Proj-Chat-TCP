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
    print("Entrada:")
    print(f"\tTexto Plano = \"{text}\";")
    print(f"\n\tTexto Plano ASCII = {text_ascii};")
    print(f"\n\tChave= {key}")
    print(f"\n\tChave ASCII = {key_ascii};")
    print(f"\n\tFluxo de chave gerado = {key_stream};")
    print(f"\n\tTexto Cript. = {encrypted_text};")
    
    return ''.join(result)

# Teste da função
rc4_key_1 = "D&Ot)[YW"
plaintext_1 = "Cybersecurity melhor disciplina do curso."
rc4(rc4_key_1, plaintext_1)

print("\n" + "-" * 40 + "\n")

rc4_key_2 = "$@C*9)6C{4^dXNw>H#W,be/'L2pM8r;JY?x}B]@A`T!q?iO`=n.Lgm(3z8@S[u]dY1k|%RI!MP-(FtZl&^3:jnK<TG6[5Jw}"
plaintext_2 = "Cybersecurity melhor disciplina do curso."
rc4(rc4_key_2, plaintext_2)

print("\n" + "-" * 40 + "\n")

rc4_key_3 = "!M|7s]u^{DFj^?8+fL:0Z!*%1P_3B}9m~V0@H^Qf7y&Z4Wb>kS^T<d.$.pL@R|g)x)-6(E&h%T-}(W%z{U9mZz8~m8BfP!c&@k7I\\5I~T_vD!4A>|oO[}3*T|$?e~0]V5&y@r1X2k+@T]j?|2|Q%}R,D)Up\\8gM;W}|7eNFk^t.h/j;6#y-!t5)\\^LJ[7S<4A,f$Ks1|&sX!w*G(Z@i>jE>6~]oA5]k'.:o=7n9h)$J_!aB{N-Jb1M}NzD\\*h"
plaintext_3 = "Cybersecurity melhor disciplina do curso."
rc4(rc4_key_3, plaintext_3)
