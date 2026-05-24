# =============================================================
# MÓDULO: modelo_produto.py
# RESPONSABILIDADE: Definição da Classe Produto (POO)
#                   POO = Programação Orientada a Objetos
#
# O que é POO? É uma forma de organizar o código usando
# "objetos" que representam coisas do mundo real.
# Aqui criamos a "planta" (classe) de como um Produto é.
# =============================================================


# ===============================================================
# CLASSE: Produto
# O QUE É: Um molde/planta para criar objetos do tipo Produto
# Cada produto terá seus próprios dados (atributos) e
# poderá executar ações (métodos)
# ===============================================================
class Produto:

    # -----------------------------------------------------------
    # MÉTODO ESPECIAL: __init__ (Construtor)
    # É chamado automaticamente quando criamos um Produto
    # 'self' representa o próprio objeto que está sendo criado
    # Os outros parâmetros são os dados do produto
    # -----------------------------------------------------------
    def __init__(self, nome, categoria, preco, quantidade, descricao="", id=None):
        # Atribuímos cada parâmetro como um ATRIBUTO do objeto
        # self.nome → cada produto tem o SEU próprio nome
        self.id = id                    # Número único do banco de dados
        self.nome = nome                # Nome do produto
        self.categoria = categoria      # Categoria (Liquida, Mercearia, Lacticinios etc.)
        self.preco = float(preco)       # Preço em reais (float)
        self.quantidade = float(quantidade) # Quantidade em estoque (float para permitir frações, ex: 0.5 kg)
        self.descricao = descricao      # Descrição opcional

    # -----------------------------------------------------------
    # MÉTODO: valor_total_estoque
    # RETORNO: float com o valor total do produto em estoque
    # O QUE FAZ: preço × quantidade
    # -----------------------------------------------------------
    def valor_total_estoque(self):
        # self.preco e self.quantidade são os atributos deste objeto
        return self.preco * self.quantidade

    # -----------------------------------------------------------
    # MÉTODO: esta_em_falta
    # RETORNO: True se a quantidade for zero, False caso contrário
    # -----------------------------------------------------------
    def esta_em_falta(self):
        return self.quantidade == 0

    # -----------------------------------------------------------
    # MÉTODO: esta_com_estoque_baixo
    # PARÂMETRO: limite → quantidade mínima considerada "baixa"
    # RETORNO: True se quantidade for menor ou igual ao limite
    # -----------------------------------------------------------
    def esta_com_estoque_baixo(self, limite=5):
        return self.quantidade <= limite and self.quantidade > 0

    # -----------------------------------------------------------
    # MÉTODO ESPECIAL: __str__
    # É chamado quando usamos str(produto) ou print(produto)
    # Retorna uma representação em texto do objeto
    # -----------------------------------------------------------
    def __str__(self):
        return (
            f"Produto: {self.nome}\n"
            f"Categoria: {self.categoria}\n"
            f"Preço: R$ {self.preco:.2f}\n"   # :.2f → 2 casas decimais
            f"Quantidade: {self.quantidade}\n"
            f"Valor em estoque: R$ {self.valor_total_estoque():.2f}"
        )

    # -----------------------------------------------------------
    # MÉTODO DE CLASSE: from_row (método fábrica)
    # PARÂMETRO: row → linha retornada pelo banco de dados
    # RETORNO: um objeto Produto criado a partir dos dados do banco
    # O decorador @classmethod indica que é um método da CLASSE,
    # não de um objeto específico
    # -----------------------------------------------------------
    @classmethod 
    def from_row(cls, row):
        # cls representa a própria classe Produto
        # Criamos e retornamos um objeto Produto com os dados do banco
        return cls(
            id=row["id"],
            nome=row["nome"],
            categoria=row["categoria"],
            preco=row["preco"],
            quantidade=row["quantidade"],
            descricao=row["descricao"] or ""  # Se NULL no banco, usa ""

            
        )