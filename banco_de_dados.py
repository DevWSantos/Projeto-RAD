

# =============================================================
# MÓDULO: banco_de_dados.py
# RESPONSABILIDADE: Toda comunicação com o banco de dados SQLite
#                   (criar tabelas, inserir, buscar, editar, deletar)
# =============================================================

# sqlite3 é uma biblioteca nativa do Python para banco de dados
# Não precisa instalar nada — já vem junto com o Python!
import sqlite3

# ---------------------------------------------------------------
# CONSTANTE: nome do arquivo do banco de dados
# O SQLite salva tudo em um único arquivo .db no seu computador
# ---------------------------------------------------------------
ARQUIVO_BANCO = "produtos.db"


# ===============================================================
# FUNÇÃO: conectar
# RETORNO: objeto de conexão com o banco de dados
# O QUE FAZ: Abre (ou cria) o arquivo de banco de dados e
#            retorna a conexão para usarmos nas outras funções
# ===============================================================
def conectar():
    # sqlite3.connect() abre o banco de dados
    # Se o arquivo não existir, ele é criado automaticamente
    conexao = sqlite3.connect(ARQUIVO_BANCO)

    # row_factory permite acessar colunas pelo nome (ex: produto["nome"])
    # em vez de por índice numérico (ex: produto[0])
    conexao.row_factory = sqlite3.Row

    return conexao  # Retornamos a conexão para quem chamou a função


# ===============================================================
# FUNÇÃO: criar_tabela
# O QUE FAZ: Cria a tabela de produtos no banco, caso ela
#            ainda não exista. É chamada uma vez ao iniciar.
# ===============================================================
def criar_tabela():
    # Abrimos a conexão com o banco
    conexao = conectar()

    # cursor é o objeto que executa os comandos SQL
    cursor = conexao.cursor()

    # Executamos o comando SQL para criar a tabela
    # IF NOT EXISTS → só cria se ainda não existir (evita erro)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT    NOT NULL,
            categoria TEXT    NOT NULL,
            preco     REAL    NOT NULL,
            quantidade INTEGER NOT NULL,
            descricao TEXT
        )
    """)
    # Explicando cada coluna:
    # id        → número único, gerado automaticamente (1, 2, 3...)
    # nome      → texto obrigatório (NOT NULL)
    # categoria → texto obrigatório
    # preco     → número decimal (REAL = float no Python)
    # quantidade→ número inteiro
    # descricao → texto opcional (pode ser NULL)

    # commit() salva as alterações no arquivo do banco
    conexao.commit()

    # Fechamos a conexão para liberar o arquivo
    conexao.close()


# ===============================================================
# FUNÇÃO: inserir_produto
# PARÂMETROS: nome, categoria, preco, quantidade, descricao
# RETORNO: True se deu certo, False se deu erro
# ===============================================================
def inserir_produto(nome, categoria, preco, quantidade, descricao=""):
    try:
        # Abrimos conexão
        conexao = conectar()
        cursor = conexao.cursor()

        # Executamos INSERT para adicionar um novo registro
        # Os '?' são placeholders — o SQLite substitui pelos valores
        # da tupla no segundo argumento. Isso evita SQL Injection!
        cursor.execute("""
            INSERT INTO produtos (nome, categoria, preco, quantidade, descricao)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, categoria, preco, quantidade, descricao))

        conexao.commit()   # Salva a inserção
        conexao.close()    # Fecha a conexão
        return True        # Sucesso!

    except Exception as erro:
        # Se qualquer erro acontecer, capturamos aqui
        print(f"Erro ao inserir produto: {erro}")
        return False  # Indica que falhou


# ===============================================================
# FUNÇÃO: listar_produtos
# RETORNO: lista com todos os produtos cadastrados
# ===============================================================
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    # SELECT * → seleciona TODAS as colunas
    # ORDER BY nome → ordena os resultados em ordem alfabética
    cursor.execute("SELECT * FROM produtos ORDER BY nome")

    # .fetchall() retorna TODOS os resultados como uma lista
    produtos = cursor.fetchall()

    conexao.close()
    return produtos  # Lista de registros (pode estar vazia)


# ===============================================================
# FUNÇÃO: buscar_produto_por_id
# PARÂMETRO: id → número inteiro do produto
# RETORNO: um único produto ou None se não encontrar
# ===============================================================
def buscar_produto_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    # WHERE id = ? → filtra apenas o produto com esse id
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))

    # .fetchone() retorna apenas UM resultado (ou None)
    # Nota: (id,) com vírgula é uma tupla de 1 elemento — obrigatório no sqlite3
    produto = cursor.fetchone()

    conexao.close()
    return produto


# ===============================================================
# FUNÇÃO: buscar_produtos_por_nome
# PARÂMETRO: texto → string de busca parcial
# RETORNO: lista de produtos cujo nome contém o texto buscado
# ===============================================================
def buscar_produtos_por_nome(texto):
    conexao = conectar()
    cursor = conexao.cursor()

    # LIKE com % → busca parcial (ex: "%ca%" encontra "caixa", "maca")
    # % antes e depois significa "qualquer coisa antes e depois do texto"
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{texto}%",))

    produtos = cursor.fetchall()
    conexao.close()
    return produtos


# ===============================================================
# FUNÇÃO: atualizar_produto
# PARÂMETROS: id + novos valores para as colunas
# RETORNO: True se deu certo, False se deu erro
# ===============================================================
def atualizar_produto(id, nome, categoria, preco, quantidade, descricao=""):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # UPDATE altera os dados de um registro existente
        # SET define quais colunas e com quais valores
        # WHERE id = ? garante que só alteramos O produto correto
        cursor.execute("""
            UPDATE produtos
            SET nome=?, categoria=?, preco=?, quantidade=?, descricao=?
            WHERE id=?
        """, (nome, categoria, preco, quantidade, descricao, id))

        conexao.commit()
        conexao.close()
        return True

    except Exception as erro:
        print(f"Erro ao atualizar produto: {erro}")
        return False


# ===============================================================
# FUNÇÃO: deletar_produto
# PARÂMETRO: id → produto a ser removido
# RETORNO: True se deu certo, False se deu erro
# ===============================================================
def deletar_produto(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # DELETE FROM remove o registro permanentemente do banco
        cursor.execute("DELETE FROM produtos WHERE id=?", (id,))

        conexao.commit()
        conexao.close()
        return True

    except Exception as erro:
        print(f"Erro ao deletar produto: {erro}")
        return False