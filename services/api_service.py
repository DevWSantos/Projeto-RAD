import threading
import requests

class APIService:
    def __init__(self, url_base):
        """
        Inicializa o serviço de API com a URL base.
        Exemplo: url_base = "https://api.exemplo.com"
        """
        self.url_base = url_base

    def notificar_assincrono(self, acao, nome_produto, texto_display="mensagem NULL"):
        """
        Método público para disparar a notificação sem travar o sistema chamador.
        """
        # 1. Monta o payload padronizado
        dados = {
            "acao": acao, 
            "produto": nome_produto, 
            "texto_display": texto_display, 
            "status_novo": True
        }

        # 2. Define a tarefa que rodará em segundo plano
        def tarefa_background():
            try:
                endpoint = f"{self.url_base}/notificar"
                
                # Faz a requisição POST com timeout de segurança
                resposta = requests.post(endpoint, json=dados, timeout=5)
                
                if resposta.status_code == 200:
                    print(f"[API SUCCESS] Ação '{acao}' para o produto '{nome_produto}' enviada!")
                else:
                    print(f"[API ERROR] Status {resposta.status_code} ao tentar '{acao}' no produto '{nome_produto}'.")
                    
            except requests.exceptions.Timeout:
                print(f"[API TIMEOUT] O servidor demorou para responder na ação '{acao}'.")
            except requests.exceptions.ConnectionError:
                print(f"[API CONNECTION ERROR] Falha de rede ao tentar '{acao}'.")
            except Exception as e:
                print(f"[API UNEXPECTED ERROR] {str(e)}")

        # 3. Cria e inicia a Thread de forma transparente para a UI
        thread_api = threading.Thread(target=tarefa_background)
        thread_api.start()