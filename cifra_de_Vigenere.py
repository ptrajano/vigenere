import os
import sys

N = 3
val_max = 15

transforma_minusculas = lambda vetor: [char.lower() if char.isalpha() and char.isascii() else char for char in vetor]

shift_vetor = lambda vetor, shift: vetor[-shift:] + vetor[:-shift]

def escrever_arquivo(file_path, conteudo):
    try:
        with open(file_path, 'w') as arquivo:
            arquivo.write(conteudo)
    except Exception as e:
        print(f"Falha ao escrever no arquivo '{file_path}': {e}")
        exit()

def ler_arquivo(file_path):
    try:
        with open(file_path, 'r') as arquivo:
            conteudo = list(arquivo.read())
    except Exception as e:
        print(f"Falha ao ler arquivo '{file_path}': {e}")
        exit()
    return conteudo

def fatores_primos(numero):
    fatores = []
    divisor = 2
    while numero > 1:
        while numero % divisor == 0:
            if divisor <= val_max:
                fatores.append(divisor)
            numero //= divisor
        divisor += 1
    return fatores

def encontrar_distancias_entre_substrings(vetor):
    ocorrencias = {} 
    distancias = [] 
    
    for indice, substring in enumerate(vetor):
        if substring in ocorrencias:
            val = indice - ocorrencias[substring]
            if val not in distancias:
                distancias.append(val)
        ocorrencias[substring] = indice
    
    return distancias

def combinacoes_possiveis(primos, atual=1, fatores=[], combinacoes=[]):
    for primo in primos:
        if atual * primo <= val_max:
            nova_combinacao = fatores + [primo]
            novo_produto = atual * primo
            if novo_produto not in combinacoes:
                combinacoes.append(novo_produto)
            combinacoes_possiveis(primos, novo_produto, nova_combinacao, combinacoes)

def definir_dicionario(dicionario):
    letras = 'abcdefghijklmnopqrstuvwxyz'
    for letra in letras:
        if letra not in dicionario:
            dicionario[letra] = 0
    dicionario = dict(sorted(dicionario.items(), key=lambda x: x[0]))
    return dicionario

def calcular_frequencia_letras(vetor):
    total_letras = sum(c.isalpha() and c.islower() for c in vetor)
    frequencia_letras = [0] * 26
    
    for letra in vetor:
        if letra.isalpha() and letra.islower():
            indice = ord(letra) - ord('a')
            frequencia_letras[indice] += 1
    
    frequencia_percentual = [(frequencia / total_letras) for frequencia in frequencia_letras]
    return frequencia_percentual

def analisar_tam_chave(cifra, tam_chave, freq):
    letras = 'abcdefghijklmnopqrstuvwxyz'

    vetores_divididos = [[] for _ in range(tam_chave)]
    for indice, elemento in enumerate(cifra):
        vetor_indice = indice % tam_chave
        vetores_divididos[vetor_indice].append(elemento)

    possivel_chave = [''] * len(vetores_divididos)

    for i, vetor in enumerate(vetores_divididos):
        max_correlacao = 0
        frequencia_letras = calcular_frequencia_letras(vetor)
        
        for j, letra in enumerate(letras):
            frequencia_letras_shifted = shift_vetor(frequencia_letras, -j)
            correlacao = sum(freq[k] * frequencia_letras_shifted[k] for k in range(len(letras)))
            if correlacao > max_correlacao:
                max_correlacao = correlacao
                chave_atual = letra

        possivel_chave[i] = chave_atual

    return ''.join(possivel_chave)

def cifragem(mensagem, chave, is_cypher = True):
    mensagem_cifrada = []
    tam_chave = len(chave)
    sinal = 1 if is_cypher else -1
    cont = 0
    for i in range(len(mensagem)):
        if mensagem[i].isalpha() and mensagem[i].isascii():
            termo = chr(ord('a') + (ord(mensagem[i]) - ord('a') + sinal * (ord(chave[cont]) - ord('a'))) % 26)
            cont = (cont + 1)%tam_chave
        else:
            termo = mensagem[i]
        mensagem_cifrada.append(termo)
    return ''.join(mensagem_cifrada)


def quebrar_cifra(cifra, freq):
    cifra_minuscula = ''.join(char for char in cifra if char.islower() and char.isascii())
    substrings = [cifra_minuscula[i:i+N] for i in range(len(cifra_minuscula) - N + 1)]
    distancias_indices = encontrar_distancias_entre_substrings(substrings)

    fatoracao_primo = set()
    
    for numero in distancias_indices:
        fatores = fatores_primos(numero)
        fatoracao_primo.update(fatores)

    combinacoes = []
    combinacoes_possiveis(fatoracao_primo, combinacoes = combinacoes)
    combinacoes = sorted(combinacoes)
    for tam_pal in combinacoes:
        if 2 < tam_pal < val_max:
            possivel_chave = analisar_tam_chave(cifra_minuscula, tam_pal, freq)
            print(f"Possivel Chave: {possivel_chave}\n")
            print(cifragem(cifra, possivel_chave, is_cypher=False))
            print("-------------------------------------------------")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Coloque a quantidade de parâmetros certo [ 'Nome do Arquivo da Mensagem', 'Nome do Arquivo de Cifra', 'chave', 'lingua']")
        exit()

    print("Escolha um Modo: ")
    print("(1) Encriptar Mensagem")
    print("(2) Decriptar Mensagem")
    print("(3) Quebrar Cifra")
    modo = int(input())
    os.system('clear')

    if modo not in (1, 2, 3):
        print("Escolhe um modo válido!")
        exit()
    
    mensagem_f = sys.argv[1]
    cifra_f = sys.argv[2]
    chave = sys.argv[3]
    lingua = sys.argv[4] 
    
    if lingua ==  'pt':
        freq = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128, 0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.0120, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021, 0.0001, 0.0047]
    elif lingua ==  'en':
        freq = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 0.0013, 0.0042, 0.0339, 0.0254, 0.0710, 0.0800, 0.0198, 0.0012, 0.0683, 0.0610, 0.1047, 0.0246, 0.0092, 0.0154	,0.0017, 0.0198, 0.0008]
    else:
        freq = [11.602/100,4.702/100,3.511/100,2.670/100,2.000/100,3.779/100,1.950/100,7.232/100,6.286/100,0.631/100,0.690/100,2.705/100,4.374/100,2.365/100,6.264/100,2.545/100,0.173/100,1.653/100,7.755/100,16.671/100,1.487/100,0.619/100,6.661/100,0.005/100,1.620/100,0.050/100]

    if modo == 1:
        mensagem = transforma_minusculas(ler_arquivo(mensagem_f))    
        cifra = cifragem(mensagem, chave)  
        escrever_arquivo(cifra_f, cifra)
    elif modo == 2:
        cifra = transforma_minusculas(ler_arquivo(cifra_f))
        mensagem = cifragem(cifra, chave, is_cypher=False)
        escrever_arquivo(mensagem_f, mensagem)   
    elif modo == 3:
        cifra = transforma_minusculas(ler_arquivo(cifra_f))
        quebrar_cifra(cifra, freq)

