#!/bin/python3

import re, sys, itertools

def inserir_separadores(cpf):
    return cpf[0]+cpf[1]+cpf[2]+"."+cpf[3]+cpf[4]+cpf[5]+"."+cpf[6]+cpf[7]+cpf[8]+"-"+cpf[9]+cpf[10]

def verificar_tipo_entrada(entrada):
    ent = re.sub('[^0-9]', '', entrada)
    # Verifica se é um CPF válido
    if re.match(r'^\d{11}$', ent):
        return 'CPF'

    # Verifica se é uma máscara de CPF
    ent = re.sub(r'\d+[%]', '', entrada)
    if len(ent) == 11:
    #if not re.match(r'^\D{11}$', ent):
        return 'Mascara de CPF'

    # Verifica se é parte de CPF
    if re.match(r'^\d{0,10}$', entrada):
        return 'Parte de CPF'

    # Tipo de entrada inválido
    return 'Inválido'

def validar_cpf(cpf):
    cpf = re.sub('[^0-9]', '', cpf)  # Remove caracteres nío numéricos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dí­gitos sío iguais
    if cpf == cpf[0] * 11:
        return False

    # Verifica o primeiro dí­gito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    if int(cpf[9]) != digito1:
        return False

    # Verifica o segundo dí­gito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    if int(cpf[10]) != digito2:
        return False

    return True

def gerar_estados(cpf):
    cpf = re.sub('[^0-9]', '', cpf)  # Remove caracteres nío numéricos
    estados = {}
    estados['DF'] = 1
    estados['GO'] = 1
    estados['MS'] = 1
    estados['MT'] = 1
    estados['TO'] = 1
    estados['AC'] = 2
    estados['AM'] = 2
    estados['AP'] = 2
    estados['PA'] = 2
    estados['RO'] = 2
    estados['RR'] = 2
    estados['CE'] = 3
    estados['MA'] = 3
    estados['PI'] = 3
    estados['DF'] = 3
    estados['AL'] = 4
    estados['PB'] = 4
    estados['PE'] = 4
    estados['RN'] = 4
    estados['BA'] = 5
    estados['SE'] = 5
    estados['MG'] = 6
    estados['ES'] = 7
    estados['RJ'] = 7
    estados['SP'] = 8
    estados['PR'] = 9
    estados['SC'] = 9
    estados['RS'] = 0
    ufs = []
    for uf in estados.keys():
        #print(estados[uf])
        if estados[uf] == int(cpf[8]):
            ufs.append(uf)
    return 'Estados de registro: ' + str(ufs)

def gerar_possibilidades_cpf(cpf):
    substring = re.sub('[^0-9]', '', cpf)
    if not substring.isdigit():
        print("A substring deve conter apenas dí­gitos numéricos.")
        return

    sstrlen = len(substring)
    compl = 11 - sstrlen

    posi = []
    for i in range(compl + 1):
        posi.append((i, compl - i))

    for pos in posi:
        for comb_prefixo in itertools.product(range(10), repeat=pos[0]):
            for comb_sufixo in itertools.product(range(10), repeat=pos[1]):
                prefixo = "".join(str(d) for d in comb_prefixo).zfill(pos[0])
                sufixo = "".join(str(d) for d in comb_sufixo).zfill(pos[1])
                cpf_gerado = prefixo + substring + sufixo
                if validar_cpf(cpf_gerado):
                    print('-> ' + cpf_gerado + ' - ' + gerar_estados(cpf_gerado))

def gerar_possibilidades_cpf_mascara(mascara):
    cpfs_possiveis = []
    indices = []
    digitos_desconhecidos = mascara.count("?")

    # Encontra os í­ndices dos dí­gitos desconhecidos na máscara
    for i, char in enumerate(mascara):
        if char == "?":
            indices.append(i)

    # Gera todas as possibilidades de CPF com base nos dí­gitos desconhecidos
    for comb in range(10 ** digitos_desconhecidos):
        cpf = mascara
        for indice, digito in zip(indices, str(comb).zfill(digitos_desconhecidos)):
            cpf = cpf[:indice] + digito + cpf[indice+1:]
        cpfs_possiveis.append(cpf)

    cpfs_possiveis.sort
    for out in cpfs_possiveis:
        if validar_cpf(out):
            print('-> ' + out + ' - ' + gerar_estados(out))



#=============================================
# INÍCIO DO SCRIPT
entrada = ''
if len(sys.argv) == 1:
    entrada = input("Digite a entrada: ")
else:
    entrada = sys.argv[1]
tipo = verificar_tipo_entrada(entrada)
print("Tipo de entrada:", tipo)
if tipo == 'CPF':
    validade = validar_cpf(entrada)
    if validade:
        print("Esse CPF é válido.")
        print(gerar_estados(entrada))
        print("Portal Transparíªncia (BR): ", "https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?termo="+entrada+"&pagina=1&tamanhoPagina=10")
        print("Situaí§ío cadastral CPF: ", "https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp")
        print("Tudo sobre todos: ", "https://tudosobretodos.info/" + entrada)
        print("Dorks interessantes:")
        print("https://www.google.com/search?q=%22"+inserir_separadores(entrada)+"%22+jusbrasil&ei=ddMoZdKBGp7d1sQP5auSyAM&oq=%22"+inserir_separadores(entrada)+"%22+jusbrasil")
    else:
        print("Esse CPF é inválido.")
elif tipo == 'Parte de CPF':
    gerar_possibilidades_cpf(entrada)
elif tipo == 'Mascara de CPF':
    gerar_possibilidades_cpf_mascara(entrada)
