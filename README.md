# 🧠 **Projeto BEM+ | _Pratique o bem. Viva a ética._** 

---
##   📌**Descrição:**

O **BEM+** é um projeto educacional e social, desenvolvido em Python, com o objetivo de incentivar boas ações, reflexões éticas e responsabilidade pessoal — especialmente voltado à área de Tecnologia da Informação.

O sistema permite que os usuários se cadastrem, respondam a dilemas éticos, participem de desafios do bem, acompanhem seu histórico de respostas e vejam seu ranking entre os colegas. Com uma abordagem leve, mas reflexiva, o BEM+ promove o desenvolvimento pessoal por meio de escolhas conscientes e ações positivas no mundo real.

---
## 🚀 **Funcionalidades (Release 2)**

- **CRUD de Usuário:**  
  - Cadastro, leitura, atualização e exclusão de contas, com dados armazenados em JSON.  
  - Pergunta secreta para recuperação de senha.

- **Frase do Dia:**  
  - Exibição diária de uma frase inspiradora, focada em positividade e bem-estar.

- **Quiz de Cenários Éticos:**  
  - Sorteio de 5 dilemas éticos por sessão, com pontuação e comentário conforme a escolha.  
  - Histórico de todas as respostas (data, pergunta, escolha e pontos).

- **Desafios do Bem:**  
  - Lista de desafios normais e premium, com validação via voucher.  
  - Geração e consumo de códigos premium em `dados/codigos_premium.json`.

- **Sistema de Pontuação & Níveis:**  
  - Pontos por quiz e desafios, níveis de “Iniciante” a “Mestre”.

- **Ranking de Usuários:**  
  - Top 5 geral exibido no menu, ordenado pela pontuação.

- **Histórico de Respostas:**  
  - Listagem completa das perguntas já respondidas, com data e resultado.

---
## 🛠️**Tecnologias Utilizadas:**

- **Linguagem:** Python 3 🐍

- **Módulos:**  
  - `os` – manipulação de arquivos e diretórios  
  - `json` – leitura e escrita de dados em JSON  
  - `re` – validação de e-mails e telefones  
  - `random` – seleção aleatória de dilemas e desafios  
  - `time` – registro de data em histórico  
 
---
##  💻**Como Instalar e Executar o BEM+**

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
## **Melhorias Futuras (Planejadas):**

- 🎨 Interface Gráfica (GUI)

- 🔐 Autenticação em Dois Fatores

- 📈 Estatísticas de Uso e Gráficos

- 🌐 Internacionalização (i18n)


### ⚠️ **Aviso:**
 *Este é o meu primeiro projeto e ainda está em desenvolvimento. Nesse sentido, o código está passando por mudanças frequentes para melhorias e correções.*