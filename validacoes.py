# =============================================================
# MÓDULO: validacoes.py
# RESPONSABILIDADE: Funções (sub-rotinas) de validação de dados
#                   Aqui verificamos se os dados digitados pelo
#                   usuário estão corretos antes de salvar no banco
# =============================================================

# re é a biblioteca de Expressões Regulares — usada para
# verificar padrões em texto (ex: somente números, só letras, etc.)
import re 


# ===============================================================
# FUNÇÃO: validar_nome
# PARÂMETRO: nome → string digitada pelo usuário
# RETORNO: (True, "") se válido | (False, "mensagem de erro") se inválido
# O QUE FAZ: Verifica se o nome tem pelo menos 2 caracteres
#            e não está vazio
# ===============================================================
def validar_nome(nome):
    # .strip() remove espaços em branco do início e fim
    nome = nome.strip()

    # Verificamos se está vazio após remover espaços
    if not nome:
        return False, "O nome do produto não pode ser vazio."

    # Verificamos o tamanho mínimo (2 letras)
    if len(nome) < 2:
        return False, "O nome deve ter pelo menos 2 caracteres."

    # Verificamos o tamanho máximo (100 letras)
    if len(nome) > 100:
        return False, "O nome deve ter no máximo 100 caracteres."

    # Se passou em todas as verificações, é válido!
    # Retornamos True e uma string vazia (sem mensagem de erro)
    return True, ""


# ===============================================================
# FUNÇÃO: validar_preco
# PARÂMETRO: preco_texto → string digitada pelo usuário
# RETORNO: (True, valor_float) se válido | (False, "erro") se inválido
# O QUE FAZ: Tenta converter o texto para número decimal
#            e verifica se é maior que zero
# ===============================================================
def validar_preco(preco_texto):
    # .strip() limpa espaços
    preco_texto = preco_texto.strip()

    if not preco_texto:
        return False, "O preço não pode ser vazio."

    # Permitimos vírgula como separador decimal (padrão brasileiro)
    # Substituímos a vírgula por ponto para o Python entender
    preco_texto = preco_texto.replace(",", ".")

    try:
        # Tentamos converter para float (número decimal)
        preco = float(preco_texto)
    except ValueError:
        # ValueError ocorre quando o texto não pode virar número
        # ex: "abc", "12.34.56", etc.
        return False, "O preço deve ser um número válido (ex: 29.90)."

    # Verificamos se o preço é maior que zero
    if preco <= 0:
        return False, "O preço deve ser maior que zero."

    # Retornamos True e o valor já convertido para float
    return True, preco


# ===============================================================
# FUNÇÃO: validar_quantidade
# PARÂMETRO: qtd_texto → string digitada pelo usuário
# RETORNO: (True, valor_int) se válido | (False, "erro") se inválido
# ===============================================================
def validar_quantidade(qtd_texto):
    qtd_texto = qtd_texto.strip()

    if not qtd_texto:
        return False, "A quantidade não pode ser vazia."

    try: 
        # float() converte para número decimal
        # Se tiver ponto (ex: "5") vai dar erro — decimal tem ponto
        quantidade = float(qtd_texto)
    except ValueError:
        return False, "A quantidade deve ser um número fracionado (ex: 10.1)."

    # Quantidade não pode ser negativa
    if quantidade < 0:
        return False, "A quantidade não pode ser negativa."

    return True, quantidade


# ===============================================================
# FUNÇÃO: validar_categoria
# PARÂMETRO: categoria → string escolhida pelo usuário
# RETORNO: (True, "") ou (False, "erro")
# ===============================================================
def validar_categoria(categoria):
    categoria = categoria.strip()

    if not categoria:
        return False, "Selecione uma categoria."

    return True, ""


# ===============================================================
# FUNÇÃO: validar_formulario_completo
# PARÂMETROS: todos os campos do formulário
# RETORNO: (True, dados_limpos) ou (False, "mensagem de erro")
# O QUE FAZ: Chama todas as validações acima e retorna
#            um dicionário com os dados já convertidos e validados
# ===============================================================
def validar_formulario_completo(nome, categoria, preco_texto, qtd_texto, descricao=""):
    # --- Validamos o nome ---
    valido, erro = validar_nome(nome)
    if not valido:
        return False, erro  # Retornamos o primeiro erro encontrado

    # --- Validamos a categoria ---
    valido, erro = validar_categoria(categoria)
    if not valido:
        return False, erro

    # --- Validamos o preço (e já pegamos o float convertido) ---
    valido, preco = validar_preco(preco_texto)
    if not valido:
        return False, preco  # Aqui 'preco' contém a mensagem de erro

    # --- Validamos a quantidade (e já pegamos o int convertido) ---
    valido, quantidade = validar_quantidade(qtd_texto)
    if not valido:
        return False, quantidade  # Aqui 'quantidade' contém a mensagem de erro

    # --- Tudo válido! Montamos o dicionário com os dados limpos ---
    dados = {
        "nome": nome.strip(),
        "categoria": categoria.strip(),
        "preco": preco,           # Já é float
        "quantidade": quantidade, # Já é int
        "descricao": descricao.strip()
    }

    return True, dados  # Retornamos True e os dados prontos para salvar