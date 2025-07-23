# 🧠 **Projeto BEM+ | _Pratique o bem. Viva a ética._** 
---

##   **Descrição:**

O **BEM+** é um projeto educacional e social, desenvolvido em Python, com o objetivo de incentivar boas ações, reflexões éticas e responsabilidade pessoal — especialmente voltado à área de Tecnologia da Informação.

O sistema, totalmente personalizado, permite que os usuários se cadastrem, respondam a dilemas éticos, participem de desafios do bem, acompanhem seu histórico de respostas e vejam um ranking com TOP 5 usuários com mais pontos. Com uma abordagem leve, mas reflexiva, o BEM+ promove o desenvolvimento pessoal por meio de escolhas conscientes e ações positivas no mundo real.

---
##  **Funcionalidades**

- **CRUD de Usuário:**  
  - Cadastro, edição, login e exclusão de contas.  
  - Armazenamento em JSON e validações robustas de entrada.  
  - Recuperação de senha via pergunta secreta e hashing seguro.

- **Frase do Dia:**  
  - Exibição decorada de uma frase motivacional.  
  - Garante uma nova frase apenas a cada dia.

- **Quiz de Cenários Éticos:**  
  - 5 dilemas sorteados por sessão.  
  - Pontuação e comentário conforme a resposta.  
  - Registro no histórico pessoal do usuário.

- **Desafios do Bem:**  
  - Lista de desafios regulares e premium.  
  - Premium requerem validação por código/voucher (ligados a ações reais).  
  - Geração e consumo de códigos controlados em `dados/codigos_premium.json`.

- **Sistema de Pontuação & Níveis:**  
  - Níveis de Iniciante 🐣 a Mestre 👑 com base em pontos.

- **Ranking de Usuários:**  
  - Exibição dinâmica dos 5 melhores usuários.  
  - Tabela com medalhas para os 3 primeiros.

- **Histórico de Respostas:**  
  - Listagem completa das perguntas já respondidas, com data, resposta e pontos.

---
## **Tecnologias Utilizadas**

- **Linguagem:** [![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

- **Bibliotecas Padrão (builtin):**
  - `os` – Manipulação de arquivos e terminal  
  - `json` – Leitura e gravação de dados persistentes  
  - `re` – Validação com expressões regulares (regex)  
  - `random` – Sorteio de dilemas e desafios  
  - `time` – Controle de delays e data atual  
  - `textwrap` – Formatação de texto no terminal

- **Biblioteca Externa:**
  - [`rich`](https://rich.readthedocs.io/en/stable/) – Interface de terminal estilizada  
    - `rich.console` – Impressão com estilos no terminal  
    - `rich.text` – Criação de textos com cores e negrito  
    - `rich.table` – Tabelas estilizadas com colunas coloridas  
    - `rich.panel` – Painéis com bordas e títulos  
    - `rich.rule` – Separadores horizontais estilizados  
    - `rich.box` – Estilos de borda para tabelas (ex: arredondado, quadrado)
  - `bcrypt` – Hashing seguro de senhas (credenciais protegidas via salt)
---

##  **Como Instalar e Executar o BEM+**

- **1 -** Verifique se possui a versão Python 3.
  Para verificar, basta digitar no seu terminal: 

```bash
python --version
```  

- **2 -** Abra um terminal na sua IDE e execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/GustavoSantosgcs/BemMais.git
```

- **3 -** Acesse a pasta BemMais

- **4 -** Instale as dependências:

```bash
pip install rich bcrypt
```

- **5 -** Execute o arquivo *main.py*

- **6 -** Pronto! Agora é só aproveitar o Bem+

---
##  **Estrutura do Projeto**
```
BemMais/
├── app/                      # Código-fonte da aplicação
│   ├── __init__.py           # Inicialização do pacote 'app'
│   ├── usuario.py            # Entidade e modelo do Usuário
│   ├── repo_usuario.py       # Repositório (JSON) com métodos CRUD
│   ├── serv_usuario.py       # Fluxo interativo de usuário (cadastro, edição, login)
│   ├── seguranca.py          # Módulo de segurança (hashing de senha com bcrypt)
│   ├── utils.py              # Funções utilitárias (input validado, limpar tela)
│   ├── frases.py             # Gerenciamento da Frase do Dia
│   ├── dilema.py             # Módulo de dilemas éticos (quiz + pontuação)
│   ├── desafios.py           # Fluxo dos Desafios do Bem (regular e premium)
│   └── ui.py                 # Interface de terminal usando Rich (menus, tabelas)
├── dados/                    # Dados persistentes em JSON
│   ├── usuarios.json         # Cadastro de usuários
│   ├── codigos_premium.json  # Vouchers dos desafios premium
│   ├── dilema.json           # Banco de dilemas éticos
│   └── frase_dia.json        # Frase exibida por dia
├── main.py                   # Ponto de entrada principal da aplicação
├── README.md                 # Documentação do projeto

```
---
## **Melhorias Futuras (Planejadas):**

-  Interface Gráfica com CustomTkInter (GUI)

-  Autenticação em Dois Fatores (2FA)

- Sistema de feedbacks dos usuários

- Ampliação do Público-Alvo para outras áreas além de TI


### ⚠️ **Aviso:**
 *Este é o meu primeiro projeto e ainda está em desenvolvimento. Assim sendo, o código está passando por mudanças frequentes para melhorias e correções.*