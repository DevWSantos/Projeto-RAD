# 📦 Projeto-CadastroPY (RAD 2026.1)

> Sistema integrado de gerenciamento de produtos com comunicação assíncrona em nuvem e feedback físico via Internet das Coisas (IoT).

## 👥 Desenvolvedores

Organizados em ordem alfabética:

* 👤 Gabriel Rodrigues Silva
* 👤 Gustavo hacker
* 👤 Kaique Barbosa
* 👤 Kauã Araújo Pires da Silva
* 👤 Uerlison Arcanjo da Silva
* 👤 Wellington Santos
* 👤 Yhllan Santana
git a
---

## 🚀 Visão Geral do Projeto

O **Projeto-CadastroPY** é um ecossistema completo de automação e controle de estoque que une uma interface de usuário rica (Desktop), uma API na nuvem e feedback em tempo real através de hardware embarcado. 

O fluxo funciona de ponta a ponta:
1. **Interface Desktop:** Desenvolvida em Python, permite gerenciar o ciclo de vida dos produtos (CRUD).
2. **API (Flask):** Recebe as ações da interface, atualiza dinamicamente um banco SQLite e gerencia uma fila inteligente de estados através do parâmetro `status_novo`.
3. **Hardware (IoT):** Um Raspberry Pi Pico W consulta a API continuamente e gera alertas visuais e sonoros imediatos baseados na ação executada.

---

## 🛠️ Arquitetura do Sistema e Repositórios

O projeto foi modularizado em três componentes independentes de forma a garantir a escalabilidade. Acesse os submódulos nos links abaixo:

| Componente | Função Principal | Link do Repositório |
| :--- | :--- | :--- |
| **Frontend Desktop** | Interface gráfica em CustomTkinter para gerenciamento de estoque (CRUD). | *Este repositório* |
| **API Backend** | Servidor Flask hospedado no Render integrado com SQLite. | [PROJETO_PYTHON_FLASK](https://github.com/Kaique-Barbosa/PROJETO_PYTHON_FLASK) |
| **Sistema Embarcado** | Código em MicroPython rodando na placa BitDogLab v6.3. | [BITDOGLAb-microPython](https://github.com/Kaique-Barbosa/BITDOGLAb-microPython) |

---

## 🧠 Lógica de Sincronização Inteligente (Fila de Comandos)

Para otimizar o uso do processamento e da rede no hardware, a API utiliza um mecanismo de controle de estado de curto período:

* **Requisição POST (Interface):** Ao cadastrar, editar ou deletar um produto, a interface atualiza uma única linha central no banco SQLite e altera o `status_novo` para `1` (True).
* **Requisição GET (Raspberry Pi Pico W):** A placa consulta a API a cada 2 segundos. 
  * Se `status_novo == 1`, a placa processa a animação correspondente e a API **altera imediatamente o status para `0` (False)** no banco.
  * Nas próximas consultas, o Pico W ignora o comando antigo, evitando repetições sonoras ou visuais desnecessárias.

---

## 🔌 Recursos de Feedback Físico (Placa BitDogLab)

Dependendo da ação recebida da nuvem, a placa BitDogLab v6.3 emite sinais exclusivos:

* **Cadastro:** Emite bipe de sucesso, acende a matriz de LED 5x5 em **Verde** e exibe os dados textuais no display OLED.
* **Atualização:** Emite melodia de update, acende a matriz de LED em **Azul** e atualiza o display OLED.
* **Exclusão:** Emite aviso sonoro de remoção, desenha uma **Lixeira estilizada** em **Laranja** nos LEDs e notifica a tela.
* **Falha de Rede:** Bipe de erro e matriz em **Vermelho** indicando perda de conexão.

---
