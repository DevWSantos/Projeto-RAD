# Guia de Integração: API REST com Tkinter (Python)

Este guia prático descreve como conectar uma interface gráfica desenvolvida em **Tkinter** a uma **API Web RESTful** utilizando a biblioteca `requests`. 

Para evitar que a interface do usuário (UI) trave ou apresente congelamentos durante o tempo de resposta da rede, este guia implementa o padrão de concorrência utilizando a biblioteca nativa `threading`.

---

## 1. Pré-requisitos

Certifique-se de instalar a biblioteca de requisições HTTP no seu ambiente de desenvolvimento virtual ou global:

```bash
pip install requests
```

---

## 2. Padrão de Arquitetura (Thread Splitting)

Ao integrar chamadas de rede em interfaces gráficas, o código deve ser segmentado em três funções com responsabilidades distintas:

1. **Gatilho da UI (Thread Principal):** Coleta as entradas dos widgets, altera o estado dos botões para evitar cliques duplicados e inicia a linha de execução paralela.
2. **Operação de Rede (Thread de Segundo Plano):** Executa a chamada HTTP, gerencia cabeçalhos/autenticação e aguarda o retorno ou estouro de tempo (*timeout*).
3. **Retorno e Atualização (Thread Principal):** Manipula de forma segura os widgets do Tkinter para exibir os dados processados ou mensagens de erro.

---

## 3. Template de Código Prático

Copie, cole e adapte a estrutura abaixo diretamente no arquivo do seu projeto:

```python
import tkinter as tk
from tkinter import messagebox
import threading
import requests

# ==========================================
# LÓGICA DA API (BACKGROUND THREAD)
# ==========================================

def executar_requisicao_api(parametro_busca):
    """
    Realiza a chamada HTTP de forma isolada para não travar a interface.
    """
    # URL de destino da sua API externa ou local
    url = f"https://api.exemplo.com/v1/dados/{parametro_busca}"
    
    # Configuração de cabeçalhos (caso sua API exija autenticação por Token)
    headers = {
        "Authorization": "Bearer SEU_TOKEN_AQUI",
        "Content-Type": "application/json"
    }

    try:
        # Faz a requisição GET com tempo limite de segurança de 5 segundos
        resposta = requests.get(url, headers=headers, timeout=5)
        
        # Converte a string de resposta JSON em um dicionário nativo do Python
        dados_json = resposta.json()

        # Validação do código de status HTTP
        if resposta.status_code == 200:
            # SUCESSO: Repassa o dicionário para a função de tratamento visual
            atualizar_interface_sucesso(dados_json)
        else:
            # ERRO DE PROTOCOLO: O servidor respondeu, mas com um código de erro (Ex: 404, 401)
            atualizar_interface_erro(f"Erro do servidor: Status {resposta.status_code}")

    except requests.exceptions.Timeout:
        atualizar_interface_erro("O servidor demorou muito para responder (Timeout).")
    except requests.exceptions.ConnectionError:
        atualizar_interface_erro("Falha de rede. Verifique sua conexão com a internet.")
    except Exception as e:
        atualizar_interface_erro(f"Ocorreu um erro inesperado: {str(e)}")


# ==========================================
# INTERAÇÃO COM A INTERFACE (UI THREAD)
# ==========================================

def disparar_busca():
    """
    Gatilho acionado pelo botão da interface. Valida e inicia o processo assíncrono.
    """
    dado_usuario = entrada_texto.get().strip()
    
    # Validação simples de preenchimento
    if not dado_usuario:
        messagebox.showwarning("Campo Vazio", "Por favor, preencha o campo de busca.")
        return

    # Bloqueia o botão para impedir múltiplas requisições paralelas concorrentes
    botao_enviar.config(state="disabled")
    label_status.config(text="Carregando dados da API...", fg="orange")

    # Instancia e inicializa a Thread assíncrona dedicada à rede
    thread_api = threading.Thread(target=executar_requisicao_api, args=(dado_usuario,))
    thread_api.start()


def atualizar_interface_sucesso(dados):
    """
    Manipula os widgets do Tkinter com os dados retornados pela API com sucesso.
    """
    # Tratamento seguro de chaves utilizando o método .get()
    resultado_nome = dados.get("nome", "Não informado")
    resultado_valor = dados.get("valor", 0.0)

    # Atualização dos elementos da interface gráfica
    label_status.config(text="Dados carregados com sucesso!", fg="green")
    label_resultado.config(text=f"Nome: {resultado_nome}\nValor: R$ {resultado_valor}")
    
    # Libera o botão novamente para novas consultas
    botao_enviar.config(state="normal")


def atualizar_interface_erro(mensagem_erro):
    """
    Notifica o usuário sobre anomalias no processo sem derrubar a aplicação.
    """
    label_status.config(text="Falha na requisição.", fg="red")
    messagebox.showerror("Erro na API", mensagem_erro)
    
    # Reativa o botão permitindo uma nova tentativa pelo usuário
    botao_enviar.config(state="normal")


# ==========================================
# CONSTRUÇÃO DA JANELA (EXEMPLO ILUSTRATIVO)
# ==========================================
root = tk.Tk()
root.title("Minha Aplicação com API")
root.geometry("400x300")

entrada_texto = tk.Entry(root, font=("Arial", 12))
entrada_texto.pack(pady=10)

botao_enviar = tk.Button(root, text="Consultar API", command=disparar_busca)
botao_enviar.pack(pady=5)

label_status = tk.Label(root, text="Aguardando comando...", fg="gray")
label_status.pack(pady=5)

label_resultado = tk.Label(root, text="", font=("Arial", 11, "bold"))
label_resultado.pack(pady=20)

root.mainloop()
```

---

## 4. Boas Práticas Fundamentais

### Acesso Seguro a Dicionários
Evite utilizar o mapeamento direto por colchetes como `dados["chave"]`. Se o payload retornado pela API omitir a propriedade por qualquer motivo, seu programa disparará uma exceção `KeyError`. Utilize obrigatoriamente `.get()`:
```python
# Recomendado: Atribui um valor padrão de Fallback caso a chave falte
cidade = dados.get("cidade", "Desconhecida")
```

### Envio de Payload (Método POST)
Se sua aplicação precisa persistir dados no servidor em vez de apenas buscá-los, modifique a chamada do verbo HTTP substituindo a propriedade `params` por `json`:
```python
dados_formulario = {"usuario": "admin", "senha": "123"}
resposta = requests.post("https://api.exemplo.com/login", json=dados_formulario, timeout=5)
```

### Parametrização de Timeout
Sempre aplique explicitamente a propriedade `timeout=X` (em segundos). Se omitido, e o barramento do servidor travar sem encerrar a conexão TCP, a aplicação Tkinter manterá uma thread fantasma alocada em memória por tempo indefinido.




mensagem = "Produto cadastrado com sucesso!"
acao_api = "cadastro"
textoDisplay = "Cadastrado com sucesso"


# CHAMADA DA CLASSE DE API EM UMA LINHA ↓↓↓↓
self.api.notificar_assincrono(acao=acao_api, nome_produto=dados["nome"], texto_display=textoDisplay)

