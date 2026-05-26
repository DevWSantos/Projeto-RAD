# =============================================================
# ARQUIVO PRINCIPAL: main.py
# RESPONSABILIDADE: Interface gráfica com Tkinter + lógica central
#                   É o arquivo que o usuário executa para
#                   iniciar o programa: python main.py
# =============================================================

# --- Importações de bibliotecas nativas do Python ---
import tkinter as tk                        # Biblioteca principal de interface gráfica
from tkinter import ttk, messagebox         # ttk = widgets modernos | messagebox = caixas de diálogo

# --- Importamos nossos próprios módulos (pacotes do projeto) ---
# Cada import abaixo carrega um arquivo .py que criamos
import banco_de_dados as bd                 # Módulo do SQLite
import validacoes as val                    # Módulo de validações
import configuracoes as cfg                 # Módulo de configurações (arquivo TXT)
from modelo_produto import Produto          # Classe Produto (POO)


# =============================================================
# CLASSE PRINCIPAL: AplicacaoCadastro
# Herda de tk.Tk → significa que ela É uma janela Tkinter
# Tudo da interface fica organizado dentro desta classe
# =============================================================
class AplicacaoCadastro(tk.Tk):

    # -----------------------------------------------------------
    # CONSTRUTOR: __init__
    # Chamado automaticamente ao criar a aplicação
    # Configura a janela, carrega dados e monta a interface
    # -----------------------------------------------------------
    def __init__(self):
        # Chamamos o construtor da classe pai (tk.Tk)
        # Isso inicializa a janela principal do Tkinter
        super().__init__()

        # --- Carregamos as configurações do arquivo TXT ---
        self.configs = cfg.carregar_configuracoes()

        # --- Configuramos a janela principal ---
        self.title(self.configs.get("nome_sistema", "Cadastro de Produtos Alimenticios"))
        self.geometry("950x600")          # Largura x Altura em pixels
        self.resizable(True, True)        # Permite redimensionar a janela
        self.configure(bg="#f0f4f8")      # Cor de fundo da janela

        # --- Inicializamos o banco de dados (cria tabela se não existir) ---
        bd.criar_tabela()

        # --- Variáveis de controle do Tkinter ---
        # StringVar() é um tipo especial que se conecta aos campos da tela
        # Quando o usuário digita, a variável atualiza automaticamente
        self.var_nome = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_preco = tk.StringVar()
        self.var_quantidade = tk.StringVar()
        self.var_descricao = tk.StringVar()
        self.var_busca = tk.StringVar()

        # Variável para guardar o ID do produto sendo editado
        # None = nenhum produto selecionado para edição
        self.produto_editando_id = None

        # --- Montamos a interface ---
        self._criar_interface()

        # --- Carregamos os produtos ao abrir o programa ---
        self.atualizar_tabela()

    # -----------------------------------------------------------
    # MÉTODO: _criar_interface
    # O QUE FAZ: Organiza todos os elementos visuais da tela
    # Convenção: métodos com _ na frente são "privados" (internos)
    # -----------------------------------------------------------
    def _criar_interface(self):
        # =========================================================
        # CABEÇALHO (topo da janela)
        # Frame = container que agrupa outros widgets
        # =========================================================
        frame_topo = tk.Frame(self, bg="#2c3e50", pady=10)
        # pack() posiciona o frame. fill=X → ocupa toda a largura
        frame_topo.pack(fill=tk.X)

        # Label = texto estático na tela
        tk.Label(
            frame_topo,
            text="📦 " + self.configs.get("nome_sistema", "Cadastro de Produtos Alimenti"),
            font=("Helvetica", 16, "bold"),  # Fonte, tamanho, estilo
            bg="#2c3e50",                     # Cor de fundo (azul escuro)
            fg="white"                        # Cor do texto (branco)
        ).pack(side=tk.LEFT, padx=20)        # Alinha à esquerda com espaçamento

        # Versão do sistema no canto direito do cabeçalho
        tk.Label(
            frame_topo,
            text=f"v{self.configs.get('versao', '1.0')}",
            font=("Helvetica", 10),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack(side=tk.RIGHT, padx=20)

        # =========================================================
        # ÁREA CENTRAL: divide em painel esquerdo (formulário)
        #               e painel direito (tabela de listagem)
        # =========================================================
        frame_central = tk.Frame(self, bg="#f0f4f8")
        frame_central.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- PAINEL ESQUERDO: Formulário de cadastro ---
        # expand=False → não expande; sticky garante que preenche o espaço
        frame_form = tk.LabelFrame(
            frame_central,
            text=" Dados do Produto ",
            font=("Helvetica", 10, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50",
            padx=10, pady=10
        )
        # side=LEFT → posiciona à esquerda | fill=Y → preenche verticalmente
        frame_form.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Chamamos o método que cria os campos do formulário
        self._criar_campos_formulario(frame_form)

        # --- PAINEL DIREITO: Tabela de produtos ---
        frame_tabela = tk.LabelFrame(
            frame_central,
            text=" Produtos Cadastrados ",
            font=("Helvetica", 10, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50",
            padx=5, pady=5
        )
        frame_tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chamamos o método que cria a tabela de listagem
        self._criar_tabela_listagem(frame_tabela)

        # =========================================================
        # RODAPÉ: exibe informações do sistema na parte inferior
        # =========================================================
        frame_rodape = tk.Frame(self, bg="#2c3e50", pady=4)
        frame_rodape.pack(fill=tk.X, side=tk.BOTTOM)

        # Label que mostrará a contagem de produtos (atualizada dinamicamente)
        self.label_status = tk.Label(
            frame_rodape,
            text="Pronto.",
            font=("Helvetica", 9),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.label_status.pack(side=tk.LEFT, padx=15)

    # -----------------------------------------------------------
    # MÉTODO: _criar_campos_formulario
    # PARÂMETRO: container → o Frame onde os campos serão colocados
    # O QUE FAZ: Cria todos os campos de entrada do formulário
    # -----------------------------------------------------------
    def _criar_campos_formulario(self, container):

        # --- Lista de categorias disponíveis ---
        categorias = [
            "Mercearia", "Frios e Laticínios", "Hortifruti", "Bebidas",
            "Limpeza", "Higiene Pessoal", "Padaria", "Congelados", "Açougue",
            "Bazar", "Rotisseria", "Outros"
        ]

        # Função auxiliar interna para criar um par Label + Entry
        def criar_campo(label_texto, variavel, linha):
            # Label descritivo à esquerda do campo
            tk.Label(
                container, text=label_texto,
                font=("Helvetica", 9), bg="#f0f4f8", anchor="w"
            ).grid(row=linha, column=0, sticky="w", pady=3)

            # Entry = campo de texto onde o usuário digita
            # textvariable conecta o campo à StringVar
            entry = tk.Entry(
                container, textvariable=variavel,
                font=("Helvetica", 10), width=22,
                relief=tk.FLAT, bd=1
            )
            entry.grid(row=linha, column=1, sticky="ew", padx=5, pady=3)
            return entry

        # Criamos os campos usando a função auxiliar acima
        # grid() posiciona em uma grade linha x coluna
        criar_campo("Nome do Produto: *", self.var_nome, 0)

        # Campo de Categoria usa Combobox (lista suspensa) em vez de Entry
        tk.Label(
            container, text="Categoria: *",
            font=("Helvetica", 9), bg="#f0f4f8", anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=3)

        # Combobox = campo com lista de opções para escolha
        self.combo_categoria = ttk.Combobox(
            container,
            textvariable=self.var_categoria,
            values=categorias,     # Opções disponíveis
            state="readonly",      # Usuário só pode escolher, não digitar
            width=20
        )
        self.combo_categoria.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        criar_campo("Preço (R$): *", self.var_preco, 2)
        criar_campo("Quantidade: *", self.var_quantidade, 3)

        # Campo descrição com Label indicando ser opcional
        tk.Label(
            container, text="Descrição:",
            font=("Helvetica", 9), bg="#f0f4f8", anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=3)

        tk.Entry(
            container, textvariable=self.var_descricao,
            font=("Helvetica", 10), width=22,
            relief=tk.FLAT, bd=1
        ).grid(row=4, column=1, sticky="ew", padx=5, pady=3)

        # Separador visual
        tk.Label(container, text="* campos obrigatórios",
                 font=("Helvetica", 8), fg="gray", bg="#f0f4f8"
                 ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0,5))

        # -------------------------------------------------------
        # BOTÕES DE AÇÃO
        # command= define qual função é chamada ao clicar
        # -------------------------------------------------------
        # Frame para agrupar os botões
        frame_botoes = tk.Frame(container, bg="#f0f4f8")
        frame_botoes.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão Salvar (verde)
        tk.Button(
            frame_botoes,
            text="💾 Salvar",
            command=self.salvar_produto,   # Chama o método salvar_produto
            bg="#27ae60", fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT, padx=10, pady=5,
            cursor="hand2"                 # Cursor vira mão ao passar sobre o botão
        ).pack(side=tk.LEFT, padx=3)

        # Botão Limpar (cinza)
        tk.Button(
            frame_botoes,
            text="🗑️ Limpar",
            command=self.limpar_formulario,
            bg="#7f8c8d", fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT, padx=10, pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=3)

        # -------------------------------------------------------
        # CAMPO DE BUSCA
        # -------------------------------------------------------
        tk.Label(
            container, text="🔍 Buscar por nome:",
            font=("Helvetica", 9, "bold"), bg="#f0f4f8"
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(15, 2))

        tk.Entry(
            container, textvariable=self.var_busca,
            font=("Helvetica", 10), width=22, relief=tk.FLAT
        ).grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        # Frame para botões de busca
        frame_busca = tk.Frame(container, bg="#f0f4f8")
        frame_busca.grid(row=9, column=0, columnspan=2, pady=5)

        tk.Button(
            frame_busca, text="Buscar",
            command=self.buscar_produto,
            bg="#2980b9", fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT, padx=8, pady=4, cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            frame_busca, text="Mostrar Todos",
            command=self.atualizar_tabela,
            bg="#8e44ad", fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT, padx=8, pady=4, cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

    # -----------------------------------------------------------
    # MÉTODO: _criar_tabela_listagem
    # PARÂMETRO: container → Frame onde a tabela será inserida
    # O QUE FAZ: Cria o Treeview (tabela visual de dados)
    # -----------------------------------------------------------
    def _criar_tabela_listagem(self, container):

        # Frame para a tabela + barra de rolagem
        frame_tree = tk.Frame(container, bg="#f0f4f8")
        frame_tree.pack(fill=tk.BOTH, expand=True)

        # Definimos as colunas da tabela
        colunas = ("id", "nome", "categoria", "preco", "quantidade", "total")

        # Treeview é o widget de tabela do Tkinter
        self.tabela = ttk.Treeview(
            frame_tree,
            columns=colunas,    
            show="headings",   # "headings" esconde a coluna vazia padrão
            height=18          # Número de linhas visíveis
        )

        # --- Definimos cabeçalho e largura de cada coluna ---
        self.tabela.heading("id",         text="ID")
        self.tabela.heading("nome",       text="Nome do Produto")
        self.tabela.heading("categoria",  text="Categoria")
        self.tabela.heading("preco",      text="Preço (R$)")
        self.tabela.heading("quantidade", text="Qtd.")
        self.tabela.heading("total",      text="Total Estoque")

        self.tabela.column("id",         width=40,  anchor="center")
        self.tabela.column("nome",       width=180, anchor="w")
        self.tabela.column("categoria",  width=100, anchor="center")
        self.tabela.column("preco",      width=80,  anchor="center")
        self.tabela.column("quantidade", width=50,  anchor="center")
        self.tabela.column("total",      width=100, anchor="center")

        # Barra de rolagem vertical (Scrollbar)
        scrollbar = ttk.Scrollbar(
            frame_tree,
            orient=tk.VERTICAL,         # Rolagem na vertical
            command=self.tabela.yview   # Conecta ao Treeview
        )
        # Conectamos o Treeview à scrollbar
        self.tabela.configure(yscrollcommand=scrollbar.set)

        # pack() posiciona tabela e scrollbar lado a lado
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Evento de duplo clique para carregar produto na edição ---
        # bind() registra uma função para ser chamada quando o evento ocorre
        # "<Double-1>" = duplo clique com o botão esquerdo do mouse
        self.tabela.bind("<Double-1>", self.ao_clicar_tabela)

        # --- Botões de ação para a tabela ---
        frame_acoes = tk.Frame(container, bg="#f0f4f8", pady=5)
        frame_acoes.pack(fill=tk.X)

        tk.Button(
            frame_acoes, text="✏️ Editar Selecionado",
            command=self.carregar_produto_para_edicao,
            bg="#f39c12", fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT, padx=8, pady=4, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_acoes, text="❌ Excluir Selecionado",
            command=self.excluir_produto,
            bg="#e74c3c", fg="white",
            font=("Helvetica", 9, "bold"),
            relief=tk.FLAT, padx=8, pady=4, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

    # ===========================================================
    # MÉTODOS DE LÓGICA (Sub-rotinas/Funções de ação)
    # São chamados pelos botões e eventos da interface
    # ===========================================================

    # -----------------------------------------------------------
    # MÉTODO: salvar_produto
    # O QUE FAZ: Lê o formulário, valida os dados e salva no banco
    #            Se produto_editando_id tiver valor, faz UPDATE
    #            Caso contrário, faz INSERT
    # -----------------------------------------------------------
    def salvar_produto(self):
        # Lemos os valores das StringVar do formulário
        nome       = self.var_nome.get()
        categoria  = self.var_categoria.get()
        preco_txt  = self.var_preco.get()
        qtd_txt    = self.var_quantidade.get()
        descricao  = self.var_descricao.get()

        # Chamamos a função do módulo validacoes para checar tudo
        valido, resultado = val.validar_formulario_completo(
            nome, categoria, preco_txt, qtd_txt, descricao
        )

        # Se a validação falhou, mostramos a mensagem de erro e paramos
        if not valido:
            # messagebox.showerror → caixa de diálogo vermelha de erro
            messagebox.showerror("Dados Inválidos", resultado)
            return  # 'return' encerra a função aqui

        # Extraímos os dados já validados e convertidos do dicionário
        dados = resultado  # 'resultado' é o dicionário quando valido=True

        # Decidimos se é inserção ou atualização
        if self.produto_editando_id is None:
            # Nenhum produto selecionado = novo cadastro
            sucesso = bd.inserir_produto(
                dados["nome"], dados["categoria"],
                dados["preco"], dados["quantidade"], dados["descricao"]
            )
            mensagem = "Produto cadastrado com sucesso!"
        else:
            # Temos um ID = atualização de produto existente
            sucesso = bd.atualizar_produto(
                self.produto_editando_id,
                dados["nome"], dados["categoria"],
                dados["preco"], dados["quantidade"], dados["descricao"]
            )
            mensagem = "Produto atualizado com sucesso!"

        if sucesso:
            # showinfo → caixa de diálogo de informação (verde/azul)
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_formulario()   # Limpa o formulário após salvar
            self.atualizar_tabela()    # Recarrega a tabela
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o produto.")

    # -----------------------------------------------------------
    # MÉTODO: limpar_formulario
    # O QUE FAZ: Apaga todos os campos do formulário e
    #            reseta o modo de edição
    # -----------------------------------------------------------
    def limpar_formulario(self):
        # .set("") limpa o valor da StringVar (e automaticamente o campo)
        self.var_nome.set("")
        self.var_categoria.set("")
        self.var_preco.set("")
        self.var_quantidade.set("")
        self.var_descricao.set("")

        # Voltamos para modo de inserção (sem produto selecionado)
        self.produto_editando_id = None

        # Atualizamos o título da janela para mostrar o modo atual
        self.title(self.configs.get("nome_sistema", "Cadastro de Produtos Alimenticios"))
        self._atualizar_status("Formulário limpo. Pronto para novo cadastro.")

    # -----------------------------------------------------------
    # MÉTODO: atualizar_tabela
    # O QUE FAZ: Busca todos os produtos no banco e exibe na tabela
    # -----------------------------------------------------------
    def atualizar_tabela(self):
        # Removemos todos os itens atuais da tabela
        # get_children() retorna todos os IDs dos itens da tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Buscamos todos os produtos no banco de dados
        produtos_rows = bd.listar_produtos()

        # Inserimos cada produto na tabela
        for row in produtos_rows:
            # Criamos um objeto Produto a partir do registro do banco
            # Isso usa o método de classe from_row que criamos em modelo_produto.py
            produto = Produto.from_row(row)

            # insert() adiciona uma linha na tabela
            # "" = inserir na raiz | tk.END = ao final da lista
            self.tabela.insert("", tk.END, values=(
                produto.id,
                produto.nome,
                produto.categoria,
                f"R$ {produto.preco:.2f}",          # Formata com 2 casas decimais
                produto.quantidade,
                f"R$ {produto.valor_total_estoque():.2f}"  # Método da classe Produto
            ))

        # Atualizamos o status no rodapé
        total = len(produtos_rows)
        self._atualizar_status(f"{total} produto(s) cadastrado(s).")

        # Limpamos o campo de busca ao mostrar todos
        self.var_busca.set("")

    # -----------------------------------------------------------
    # MÉTODO: buscar_produto
    # O QUE FAZ: Busca produtos pelo nome e exibe na tabela
    # -----------------------------------------------------------
    def buscar_produto(self):
        texto = self.var_busca.get().strip()

        # Se não digitou nada, mostra todos
        if not texto:
            self.atualizar_tabela()
            return

        # Limpamos a tabela atual
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Buscamos no banco pelo nome parcial
        resultados = bd.buscar_produtos_por_nome(texto)

        for row in resultados:
            produto = Produto.from_row(row)
            self.tabela.insert("", tk.END, values=(
                produto.id,
                produto.nome,
                produto.categoria,
                f"R$ {produto.preco:.2f}",
                produto.quantidade,
                f"R$ {produto.valor_total_estoque():.2f}"
            ))

        total = len(resultados)
        self._atualizar_status(f"{total} resultado(s) para '{texto}'.")

    # -----------------------------------------------------------
    # MÉTODO: ao_clicar_tabela
    # PARÂMETRO: event → informações do evento de clique
    # O QUE FAZ: Detecta duplo clique na tabela e carrega o produto
    # -----------------------------------------------------------
    def ao_clicar_tabela(self, event):
        # Simplesmente delegamos para o método de edição
        self.carregar_produto_para_edicao()

    # -----------------------------------------------------------
    # MÉTODO: carregar_produto_para_edicao
    # O QUE FAZ: Pega o produto selecionado na tabela e
    #            preenche o formulário para edição
    # -----------------------------------------------------------
    def carregar_produto_para_edicao(self):
        # selection() retorna os itens selecionados na tabela
        selecionados = self.tabela.selection()

        # Verificamos se há algum item selecionado
        if not selecionados:
            messagebox.showwarning("Atenção!", "Selecione um produto na tabela.")
            return

        # Pegamos o primeiro item selecionado (índice 0)
        item = selecionados[0]

        # item(..., "values") retorna os valores das colunas daquela linha
        valores = self.tabela.item(item, "values")

        # O ID é o primeiro valor (índice 0)
        produto_id = int(valores[0])

        # Buscamos o produto completo no banco pelo ID
        row = bd.buscar_produto_por_id(produto_id)

        if row:
            produto = Produto.from_row(row)

            # Preenchemos cada campo do formulário com os dados do produto
            self.var_nome.set(produto.nome)
            self.var_categoria.set(produto.categoria)
            self.var_preco.set(str(produto.preco))
            self.var_quantidade.set(str(produto.quantidade))
            self.var_descricao.set(produto.descricao)

            # Guardamos o ID para saber que estamos em modo de edição
            self.produto_editando_id = produto.id

            # Atualizamos o título para indicar modo edição
            self.title(f"Editando: {produto.nome}")
            self._atualizar_status(f"Editando produto ID {produto.id}: {produto.nome}")

    # -----------------------------------------------------------
    # MÉTODO: excluir_produto
    # O QUE FAZ: Remove o produto selecionado da tabela e do banco
    # -----------------------------------------------------------
    def excluir_produto(self):
        selecionados = self.tabela.selection()

        if not selecionados:
            messagebox.showwarning("Atenção!", "Selecione um produto para excluir.")
            return

        # Pegamos o nome e ID do produto selecionado
        valores = self.tabela.item(selecionados[0], "values")
        produto_id = int(valores[0])
        nome_produto = valores[1]

        # askyesno → caixa de diálogo com Sim/Não para confirmação
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja excluir o produto:\n'{nome_produto}'?\n\nEsta ação não pode ser desfeita."
        )

        # Só excluímos se o usuário confirmou
        if confirmar:
            sucesso = bd.deletar_produto(produto_id)

            if sucesso:
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.limpar_formulario()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir o produto.")

    # -----------------------------------------------------------
    # MÉTODO: _atualizar_status
    # PARÂMETRO: mensagem → texto a exibir no rodapé
    # O QUE FAZ: Atualiza o label de status no rodapé da janela
    # -----------------------------------------------------------
    def _atualizar_status(self, mensagem):
        # .config() altera propriedades de um widget após sua criação
        self.label_status.config(text=mensagem)


# =============================================================
# PONTO DE ENTRADA DO PROGRAMA
#
# Este bloco só executa se rodarmos ESTE arquivo diretamente
# (python main.py). Se outro arquivo importar main.py,
# este bloco NÃO executa — isso é fundamental em Python!
# =============================================================
if __name__ == "__main__":
    # Criamos a aplicação (chama __init__ da classe)
    app = AplicacaoCadastro()

    # mainloop() mantém a janela aberta e "ouvindo" eventos
    # (cliques, digitação, etc.) até o usuário fechar a janela
    app.mainloop()