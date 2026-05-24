
import sqlite3


ARQUIVO_BANCO = "produtos.db"



def conectar():
    
    # Se o arquivo não existir, ele é criado automaticamente
    conexao = sqlite3.connect(ARQUIVO_BANCO)

    
    conexao.row_factory = sqlite3.Row

    return conexao  


# ===============================================================
# FUNÇÃO: criar_tabela
# ===============================================================
def criar_tabela():
   
    conexao = conectar()

  
    cursor = conexao.cursor()

  
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
    
    # id        → número único, gerado automaticamente 
    # nome      → texto obrigatório 
    # preco     → número decimal 
    # quantidade→ número inteiro
    # descricao → texto opcional 

    
    conexao.commit()

    
    conexao.close()


# ===============================================================
# FUNÇÃO: inserir_produto
# ===============================================================
def inserir_produto(nome, categoria, preco, quantidade, descricao=""):
    try:
        
        conexao = conectar()
        cursor = conexao.cursor()

        
        cursor.execute("""
            INSERT INTO produtos (nome, categoria, preco, quantidade, descricao)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, categoria, preco, quantidade, descricao))

        conexao.commit()   
        conexao.close()   
        return True        

    except Exception as erro:
        
        print(f"Erro ao inserir produto: {erro}")
        return False  


# ===============================================================
# FUNÇÃO: listar_produtos
# ===============================================================
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    # SELECT * 
    # ORDER BY nome 
    cursor.execute("SELECT * FROM produtos ORDER BY nome")

    # .fetchall() 
    produtos = cursor.fetchall()

    conexao.close()
    return produtos  # Lista de registros (pode estar vazia)


# ===============================================================
# FUNÇÃO: buscar_produto_por_id
# ===============================================================
def buscar_produto_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

   
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))

    # .fetchone() retorna apenas UM resultado (ou None)
    
    produto = cursor.fetchone()

    conexao.close()
    return produto


# ===============================================================
# FUNÇÃO: buscar_produtos_por_nome
# ===============================================================
def buscar_produtos_por_nome(texto):
    conexao = conectar()
    cursor = conexao.cursor()

    # LIKE com % → busca parcial (ex: "%ca%" encontra "caixa", "maca")
   
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{texto}%",))

    produtos = cursor.fetchall()
    conexao.close()
    return produtos


# ===============================================================
# FUNÇÃO: atualizar_produto
# ===============================================================
def atualizar_produto(id, nome, categoria, preco, quantidade, descricao=""):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        
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
# ===============================================================
def deletar_produto(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        
        cursor.execute("DELETE FROM produtos WHERE id=?", (id,))

        conexao.commit()
        conexao.close()
        return True

    except Exception as erro:
        print(f"Erro ao deletar produto: {erro}")
        return False