
# re é a biblioteca de Expressões Regulares — usada para

import re 


# ===============================================================
# FUNÇÃO: validar_nome
# ===============================================================
def validar_nome(nome):
    # .strip() remove espaços em branco do início e fim
    nome = nome.strip()

   
    if not nome:
        return False, "O nome do produto não pode ser vazio."

   
    if len(nome) < 2:
        return False, "O nome deve ter pelo menos 2 caracteres."

   
    if len(nome) > 100:
        return False, "O nome deve ter no máximo 100 caracteres."

    # Retornamos True e uma string vazia (sem mensagem de erro)
    return True, ""


# ===============================================================
# FUNÇÃO: validar_preco
# ===============================================================
def validar_preco(preco_texto):
    # .strip() limpa espaços
    preco_texto = preco_texto.strip()

    if not preco_texto:
        return False, "O preço não pode ser vazio."

    
        preco = float(preco_texto)
    except ValueError:
       
    return False, "O preço deve ser um número válido (ex: 29.90)."

   
    if preco <= 0:
        return False, "O preço deve ser maior que zero."

  
    return True, preco


# ===============================================================
# FUNÇÃO: validar_quantidade
# ===============================================================
def validar_quantidade(qtd_texto):
    qtd_texto = qtd_texto.strip()

    if not qtd_texto:
        return False, "A quantidade não pode ser vazia."

    try: 
        
        quantidade = float(qtd_texto)
    except ValueError:
        return False, "A quantidade deve ser um número fracionado (ex: 10.1)."

    
    if quantidade < 0:
        return False, "A quantidade não pode ser negativa."

    return True, quantidade


# ===============================================================
# FUNÇÃO: validar_categoria
# ===============================================================
def validar_categoria(categoria):
    categoria = categoria.strip()

    if not categoria:
        return False, "Selecione uma categoria."

    return True, ""


# ===============================================================
# FUNÇÃO: validar_formulario_completo
# ===============================================================
def validar_formulario_completo(nome, categoria, preco_texto, qtd_texto, descricao=""):
    # --- Validamos o nome ---
    valido, erro = validar_nome(nome)
    if not valido:
        return False, erro  
   
    valido, erro = validar_categoria(categoria)
    if not valido:
        return False, erro

   
    valido, preco = validar_preco(preco_texto)
    if not valido:
        return False, preco  

    
    valido, quantidade = validar_quantidade(qtd_texto)
    if not valido:
        return False, quantidade  

    
    dados = {
        "nome": nome.strip(),
        "categoria": categoria.strip(),
        "preco": preco,           # Já é float
        "quantidade": quantidade, # Já é int
        "descricao": descricao.strip()
    }

    return True, dados  