# 🧠 **Projeto BEM+ | _Pratique o bem. Viva a ética._** 
---

##   **Descrição:**

O **BEM+** é um projeto educacional e social, desenvolvido em Python, com o objetivo de incentivar boas ações, reflexões éticas e responsabilidade pessoal — especialmente voltado à área de Tecnologia da Informação.

O sistema permite que os usuários se cadastrem, respondam a dilemas éticos, participem de desafios do bem, acompanhem seu histórico de respostas e vejam um ranking com TOP 5 usuários com mais pontos. Com uma abordagem leve, mas reflexiva, o BEM+ promove o desenvolvimento pessoal por meio de escolhas conscientes e ações positivas no mundo real.

---
##  **Funcionalidades**

- **CRUD de Usuário:**  
  - Cadastro, leitura, atualização e exclusão de contas, com dados armazenados em JSON.  
  - Pergunta secreta para recuperação de senha.

- **Frase do Dia:**  
  - Exibição diária de uma frase inspiradora, focada em positividade e bem-estar.

- **Quiz de Cenários Éticos:**  
  - Sorteio de 5 dilemas éticos por sessão, com pontuação e comentário conforme a escolha.  

- **Desafios do Bem:**  
  - Lista de desafios regulares e desafios premium (os desafios premium são relacionados a outros projetos da turma e solicitam validação via voucher para confirmar conclusão).  
  - Geração e consumo de códigos premium em `dados/codigos_premium.json`.

- **Sistema de Pontuação & Níveis:**  
  - Pontos por quiz e desafios, níveis de “Iniciante” a “Mestre”.

- **Ranking de Usuários:**  
  - Top 5 geral exibido no menu, ordenado pela pontuação.

- **Histórico de Respostas:**  
  - Listagem completa das perguntas já respondidas, com data, resposta e pontos.

---
## **Tecnologias Utilizadas**

- **Linguagem:** [![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

- **Módulos:**  
  - `os` – manipulação de arquivos e diretórios  
  - `json` – leitura e escrita de dados em JSON  
  - `re` – validação de e-mails e telefones  
  - `random` – seleção aleatória de dilemas e desafios  
  - `time` – registro de data em histórico  
  - `textwrap` – formatação de texto para terminal  
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

- **4 -** Execute o arquivo *main.py*

- **5 -** Pronto! Agora é só aproveitar o Bem+

---
##  **Estrutura do Projeto**
```
BemMais/
├── app/                         ── Código-fonte da aplicação
│   ├── __init__.py              ── Inicialização do pacote 'app'
│   ├── usuario.py               ── Entidade e modelo Usuário
│   ├── repo_usuario.py          ── Repositório de Usuário (JSON)
│   ├── serv_usuario.py          ── Serviços de cadastro, edição e recuperação
│   ├── utils.py                 ── Utilitários (limpar tela, input, prints)
│   ├── frases.py                ── Lógica de "Frase do Dia"
│   ├── dilema.py                ── Quiz de cenários éticos
│   ├── desafios.py              ── Fluxo de "Desafios do Bem"
│   └── ui.py                    ── Camada de apresentação (Rich)
├── dados/                        # JSONs de dados persistidos
│   ├── usuarios.json             # Usuários cadastrados
│   ├── codigos_premium.json      # Vouchers dos desafios premium
│   ├── dilema.json               # Definições de cenários éticos
│   └── frase_dia.json            # Frase do dia (persistência diária)
├── main.py                      ── Ponto de entrada da aplicação ('BemMais')
├── README.md                    ── Documentação do projeto

```
---
## **Melhorias Futuras (Planejadas):**

-  Interface Gráfica (GUI)

-  Autenticação em Dois Fatores

-  Estatísticas de Uso e Gráficos


### ⚠️ **Aviso:**
 *Este é o meu primeiro projeto e ainda está em desenvolvimento. Assim sendo, o código está passando por mudanças frequentes para melhorias e correções.*