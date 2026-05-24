# =============================================================
# MÓDULO: configuracoes.py
# RESPONSABILIDADE: Ler e salvar configurações do sistema em
#                   arquivo TXT (requisito obrigatório do projeto)
# =============================================================

# Importamos 'os' para verificar se o arquivo existe no computador
import os

# ---------------------------------------------------------------
# CONSTANTE: nome do arquivo de configurações
# Usar caixa alta (MAIÚSCULO) é uma convenção para constantes em Python
# ---------------------------------------------------------------
ARQUIVO_CONFIG = "config.txt"

# ---------------------------------------------------------------
# CONFIGURAÇÕES PADRÃO
# Dicionário usado quando o arquivo ainda não existe
# ---------------------------------------------------------------
CONFIGURACOES_PADRAO = {
    "nome_sistema": "Sistema de Cadastro de Produtos",
    "versao": "1.0",
    "tema": "claro",
    "max_produtos": "1000"
}


# ===============================================================
# FUNÇÃO: salvar_configuracoes
# PARÂMETRO: configs → dicionário com as configurações a salvar
# O QUE FAZ: Percorre o dicionário e escreve cada par
#            chave=valor em uma linha do arquivo TXT
# ===============================================================
def salvar_configuracoes(configs):
    # Abrimos o arquivo em modo escrita ('w')
    # 'w' apaga o conteúdo anterior e começa do zero
    # encoding='utf-8' garante que acentos funcionem corretamente
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as arquivo:
        # Percorremos cada chave e valor do dicionário
        for chave, valor in configs.items():
            # Escrevemos no formato: chave=valor\n
            # \n é a quebra de linha (pula para a próxima linha)
            arquivo.write(f"{chave}={valor}\n")


# ===============================================================
# FUNÇÃO: carregar_configuracoes
# RETORNO: dicionário com as configurações lidas do TXT
# O QUE FAZ: Lê o arquivo TXT linha por linha e monta um
#            dicionário. Se o arquivo não existir, usa o padrão.
# ===============================================================
def carregar_configuracoes():
    # Verificamos se o arquivo de config já existe
    if not os.path.exists(ARQUIVO_CONFIG):
        # Se não existe, salvamos as configurações padrão e as retornamos
        salvar_configuracoes(CONFIGURACOES_PADRAO)
        return CONFIGURACOES_PADRAO.copy()  # .copy() evita modificar o original

    # Criamos um dicionário vazio para armazenar o que vamos ler
    configs = {}

    # Abrimos o arquivo em modo leitura ('r')
    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as arquivo:
        # Lemos todas as linhas de uma vez
        for linha in arquivo.readlines():
            # .strip() remove espaços e \n do início e fim da linha
            linha = linha.strip()

            # Ignoramos linhas vazias
            if not linha:
                continue

            # Separamos a linha no símbolo '=' em duas partes:
            # ex: "tema=claro" → chave="tema", valor="claro"
            # maxsplit=1 garante que só dividimos no PRIMEIRO '='
            partes = linha.split("=", maxsplit=1)

            # Verificamos se a linha tem exatamente 2 partes (chave e valor)
            if len(partes) == 2:
                chave = partes[0].strip()   # Remove espaços extras da chave
                valor = partes[1].strip()   # Remove espaços extras do valor
                configs[chave] = valor      # Adiciona no dicionário

    return configs  # Retornamos o dicionário preenchido