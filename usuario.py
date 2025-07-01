import json
import os
import re

CAMINHO = os.path.join('dados', 'usuarios.json')


class RepoUsuario:
     """ Carrega, salva e gerencia todos os objetos do Usuario."""
     
     def __init__(self):
          """
          Inicializa o repositório de usuários em memória.

          Carrega os dados do arquivo JSON (CAMINHO) para o dicionário interno
          self.usuarios. Se o arquivo não existir ou estiver corrompido,
          inicia com base vazia.
          """
          self.usuarios = self.carregar_usuarios()
          
     
     # Carregar usuários:
     def carregar_usuarios(self): 
        """Lê o JSON (se existir) e devolve dict de objetos Usuario."""
        if os.path.exists(CAMINHO):
            try:
                with open(CAMINHO, "r", encoding="utf-8") as arq:
                    arq_bruto = json.load(arq)
                    return {key_email: Usuario.from_dict(d) for key_email, d in arq_bruto.items()}
            except (json.JSONDecodeError, IOError):
                print("⚠️ Erro ao ler arquivo JSON. Iniciando base vazia.")
        return {}
   
   
     #Salvar usuários:
     def salvar_usuarios(self):
          """Serializa o dicionário em memória para o JSON."""
          os.makedirs(os.path.dirname(CAMINHO), exist_ok=True)
          arq_bruto = {}
          for key_email, user in self.usuarios.items():
               dicio_do_usuario = user.to_dict()
               arq_bruto[key_email] = dicio_do_usuario
               
          with open(CAMINHO, "w", encoding="utf-8") as arq:
               json.dump(arq_bruto, arq, indent=4, ensure_ascii=False)


     # Método cadastrar:
     def cadastrar(self, usuario):
          if usuario.email in self.usuarios:
               raise ValueError("Email já cadastrado.")
          self.usuarios[usuario.email] = usuario
          self.salvar_usuarios()


     # Buscar usuários:
     def buscar(self, email):
          """
          Busca um usuário pelo email.

          Parâmetros:
          email (str): email do usuário a ser pesquisado.

          Retorna:
          Usuario: instância encontrada, ou None se não existir.
          """
          return self.usuarios.get(email)


     # Listar usuários:
     def listar(self):
          """
          Retorna todos os usuários cadastrados.

          Retorna:
               list[Usuario]: lista com todos os objetos Usuario do repositório.
          """
          return list(self.usuarios.values())


     #Remover usuários:
     def remover(self, email):
          """
          Remove o usuário identificado pelo email do repositório e atualiza o JSON.

          Parâmetros:
          email (str): email do usuário a ser removido.
          """
          if email in self.usuarios:
               del self.usuarios[email]
               self.salvar_usuarios()


     # Atualizar email (método):
     def atualizar_email(self, email, novo_email):
          """
          Atualiza a chave do usuário de 'email' para 'novo_email' e persiste.

          Parâmetros:
          email (str): email atual do usuário.
          novo_email (str): novo email a ser atribuído.

          Lança (raise):
          ValueError: se 'novo_email' já estiver cadastrado ou 'email' não existir.
          """
          
          if novo_email in self.usuarios:
               raise ValueError("Novo email digitado já está cadastrado.")
          usuario = self.usuarios.pop(email)
          usuario.email = novo_email
          self.usuarios[novo_email] = usuario
          self.salvar_usuarios()


# Classe usuário:
class Usuario:         
     def __init__(self, nome, telefone, email, senha, pontos=0, resposta_secreta=None,
                     desafios_realizados=None, historico_respostas=None):
          """
          Constrói um novo usuário e vlaida seus daados iniciais.
          
          Parâmetros:
            nome (str).
            telefone (str).
            email (str): email válido (@ufrpe.br, @gmail.com, etc.).
            senha (str): senha numérica de 6 dígitos.
            pontos (int): pontuação inicial (default=0).
            resposta_secreta (str|None): resposta para recuperação de senha.
            desafios_realizados (list|None): lista inicial de códigos de desafios.
            historico_respostas (list|None): lista inicial de respostas.

        Lança (raise):
            ValueError: se qualquer dado de entrada não passar nas validações.
          """
          if not self.email_valido(email):
               raise ValueError("Email digitado é inválido.")
          if not self.senha_valida(senha):
               raise ValueError("Senha digitada é inválida")
          if not self.telefone_valido(telefone):
               raise ValueError("Telefone digitado é inválido!")                    
                    
          self.nome = nome
          self.telefone = telefone
          self.email = email
          self.senha = senha
          self.pontos = pontos
          self.resposta_secreta = resposta_secreta
          self.desafios_realizados = list(desafios_realizados) if desafios_realizados is not None else []
          self.historico_respostas = list(historico_respostas) if historico_respostas is not None else []


     # Serialização:
     def to_dict(self):
               """Converte o objeto para um dicionário JSON."""
               return {
                    "nome": self.nome,
                    "telefone": self.telefone,
                    "email": self.email,
                    "senha": self.senha,
                    "pontos": self.pontos,
                    "resposta_secreta": self.resposta_secreta,
                    "desafios_realizados": self.desafios_realizados,
                    "historico_respostas": self.historico_respostas,
               }
               
               
     # Deserialização:           
     @classmethod
     def from_dict(cls, dados):
          """Cria um Usuario a partir de um dicionário (caminho inverso do to_dict)."""
          return cls(**dados) # '**' espalha as chaves/valores como argumentos nomeados para o __init__. 


     # Validação de telefone:
     @staticmethod
     def telefone_valido(telefone):
          """
          Verifica se o telefone informado possui um formato padrão do Brasil.
          Aceita o número com o sem espaço após o DDD
          Ex.:(81) 98877-4422 ou (81)98877-4422
          
          Parâmetros:
          telefone (str): telefone informado pelo usuário.
          
          Retorna:
          bool: True se o telefone estiver valido, False caso negativo.
          """
          padrao = r'^\([1-9]{2}\)\s?9[0-9]{4}-[0-9]{4}$'
          return re.match(padrao,telefone) is not None


     # Validação de email:
     @staticmethod
     def email_valido(email):
         """
         Verifica se o email possui um formato válido e pertence a um domínio permitido.
     
         Parâmetros:
         email (str): Email informado pelo usuário.
     
         Retorna:
         bool: True se o email for válido, False caso contrário.
         """
         padrao = r'^[\w\.-]+@(?:gmail\.com|hotmail\.com|outlook\.com|ufrpe\.br)$'
         return re.match(padrao, email) is not None
      
          
     # Validação de senha:
     @staticmethod
     def senha_valida(senha):
          """
          Verifica se a senha contém apenas dígitos e tem 6 caracteres.

          Parâmetros:
          senha (str): Senha informada pelo usuário.

          Retorna:
          bool: True se a senha for válida, False caso contrário.
          """
          return senha.isdigit() and len(senha) == 6


     # Alterar email:
     def alterar_email(self, novo_email):
          """
          Realiza o fluxo interativo de alteração de email no terminal.

          Parâmetros:
               novo_email (str): novo endereço de email a ser atribuído.
          
          Lança:
               ValueError: se o formato de email for inválido ou vazio.
          """
          if not Usuario.email_valido(novo_email):
               raise ValueError("Formato de email inválido!")
          self.email = novo_email


     # Alteração de senha:
     def alterar_senha(self, senha_atual, nova_senha):
          """
           Atualiza a senha do usuário, conferindo a senha atual.
          
          Parâmetros:
               senha_atual (str): senha atual do usuário para autenticação.
               nova_senha (str): nova senha numérica de exatamente 6 dígitos.

          Lança (raise):
               ValueError – se a senha atual não confere ou nova senha for inválida.
          """
          if senha_atual != self.senha:
               raise ValueError("Senha atual incorreta.")
          
          if not self.senha_valida(nova_senha):
               raise ValueError("Nova senha inválida (seis dígitos numéricos).")
          self.senha = nova_senha


     # Alterar resposta secreta:
     def alterar_resposta(self, nova_resposta):
          """
          Permite ao usuário alterar a resposta secreta usada para recuperação de senha.

          Parâmetros:
               nova_resposta (str): nova resposta não vazia.

          Lança:
               ValueError: se `nova_resposta` for string vazia.
          """
          self.resposta_secreta = nova_resposta
          

# Teste de entrada (input não vazio):
def nao_vazio(mensagem):
    """Looping até o usuário digitar algo diferente de vazio."""
    while True:
        if texto := input(mensagem).strip():   # walrus 
            return texto.strip()
        print("Entrada vazia. Tente novamente.\n")


#Cadastro de usuário:
def cadastrar_usuario(repo: RepoUsuario):
     """
     Realiza o cadastro de um novo usuário com nome, telefone, email, senha e pergunta secreta.

     Parâmetros:
          repo (RepoUsuario): repositório para persistir o novo usuário.
     """ 
     
     while True: # looping externo de cadastro
          nome = nao_vazio("Digite seu nome de usuário: ").title()
          telefone = nao_vazio("Digite seu telefone com DDD Ex:(81) 9xxxx-xxxx: ")
          while not Usuario.telefone_valido(telefone):
               print("Erro de digitação!")
               telefone = nao_vazio(" Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
          
          while True:  
               email = nao_vazio("Digite seu email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
               if not Usuario.email_valido(email):
                    print("Formato de email inválido!")
                    continue
               if repo.buscar(email):   
                    print("Email já cadastrado!")
                    return
               else:
                    break    
                         
          while True:     
               senha = nao_vazio("Digite uma senha com 6 digitos (apenas números): ")
               if not Usuario.senha_valida(senha):
                    print("Senha inválida! Tente novamente.")
                    continue
               confirmação = nao_vazio("Confirme a senha")
               if confirmação == senha:
                    print("Perfeito! Senhas iguais.")
                    break
               else:
                    print("Senhas diferentes! Tente novamente...")
               
          print("\nPara recuperação de senha, responda a seguinte pergunta: ")   
          resposta_secreta = nao_vazio("Qual o nome da sua professora favorita? ")
                 
          try:
               novo = Usuario(
                    nome=nome,
                    telefone=telefone,
                    email=email,
                    senha=senha,
                    resposta_secreta=resposta_secreta
               )
          except ValueError as msg_erro: # Se Alguma validação do __init__ falhou 
               print("Erro:", msg_erro)
               print("Vamos tentar de novo...\n")
               continue  
          
          try:
            repo.cadastrar(novo)
            print("✅ Cadastro realizado com sucesso!\n")
            break
          except ValueError as msg_erro: # Verifica novamente se o email já é cadastrado
            print(msg_erro)
               

# Fluxo de alteração de senha:     
def fluxo_alterar_senha(repo: RepoUsuario, email):
     """
     Fluxo para alterar a senha do usuário logado.

     Parâmetros:
          repo (RepoUsuario): repositório que persiste as mudanças.
          email (str): email do usuário que está logado.
     """
     user = repo.buscar(email)

     while True:
          senha_atual = nao_vazio("Digite sua senha atual: ")
          nova_senha  = nao_vazio("Nova senha (6 dígitos numericos): ")
          confirmar_senha = nao_vazio("Confirme a nova senha: ")

          if nova_senha != confirmar_senha:
               print("Senhas diferentes! Tente de novo.\n")
               continue

          try:
               user.alterar_senha(senha_atual, nova_senha)   
               repo.salvar_usuarios()            
               print("Senha atualizada com sucesso!\n")
               break
          except ValueError as msg_erro:
               print(msg_erro, "\n")


# Fluxo de alteração de email:
def fluxo_alterar_email(repo: RepoUsuario, email):
     """
     Fluxo para alterar o email do usuário logado.

     Parâmetros:
          repo (RepoUsuario): repositório que persiste as mudanças.
          email (str): email atual do usuário que está logado.

     Retorna:
          str: o novo email em caso de sucesso, ou o email original em erro.
     """
     novo_email = nao_vazio("Digite o novo email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
     if not Usuario.email_valido(novo_email):
          print("Formato de email inválido!")
          return email
     try:
          repo.atualizar_email(email, novo_email)
          print("✔  Seu email foi atualizado!")
          return novo_email
     
     except ValueError as erro:
          print("Erro: ",erro)
          return email


# Fluxo de alteração da resposta secreta:
def fluxo_alterar_resposta(repo: RepoUsuario, email):
     """
     Fluxo para alterar a resposta secreta do usuário logado.

     Parâmetros:
          repo (RepoUsuario): repositório que persiste as mudanças.
          email (str): email do usuário que está logado.
     """
     user = repo.buscar(email)
     senha = nao_vazio("Confirme sua senha atual: ")
     if senha != user.senha:
          print("Senha incorreta! Voltando ao menu...")
          return
     
     nova_resposta = nao_vazio("Digite a nova resposta secreta (professora favorita): ")
     try:
          user.alterar_resposta(nova_resposta)
          repo.salvar_usuarios()
          print("✔  Resposta secreta atualizada com sucesso!")
          
     except ValueError as erro:
          print("Erro: ",erro)

        
# Editar usuario:
def editar_conta(repo: RepoUsuario,email):
     """
     Permite ao usuário logado editar suas informações pessoais.

     Parâmetros:
        repo (RepoUsuario): repositório que contém e persiste os usuários.
        email (str): email atual do usuário logado.
     Retorna:
          o email atualizado (ou o original, se não alterar).
     """
     user = repo.buscar(email)
     print("\nDados atuais:\n")
     print(f"Email: {user.email}")
     print(f"Nome: {user.nome}")
     print(f"Telefone: {user.telefone}")
     while True:
          print("\nO que deseja editar: ")
          print("1 - email")
          print("2 - nome")
          print("3 - telefone")
          print("4 - senha")
          print("5 - Resposta_secreta")
          print("0 - sair")
          editar = input("opção: ")
          match editar:
               case '1': 
                    novo_email = fluxo_alterar_email(repo, email)
                    return novo_email     
               case '2':
                    novo_nome = nao_vazio("Digite o novo nome: ").title()
                    user.nome = novo_nome
                    repo.salvar_usuarios()
                    print("✔ Nome atualizado com sucesso!")
                    
               case '3':
                    novo_tel = nao_vazio("Digite o novo número de telefone com DDD Ex:(81) 99999-8888: ")
                    while not user.telefone_valido(novo_tel):
                         print("Formato inválido!")
                         novo_tel = nao_vazio("Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
                    
                    user.telefone = novo_tel
                    repo.salvar_usuarios()
                    print("✔ Telefone atualizado com sucesso!")
                    
               case '4':
                    fluxo_alterar_senha(repo, email)
                    
               case '5':
                    fluxo_alterar_resposta(repo, email)
               
               case '0':
                    print("Vamos voltar então...\n")
                    break
               
               case _:
                    print("Opção inválida!")        
     return email


# Recuperar senha:
def recuperar_senha(repo: RepoUsuario):
     """
     Permite ao usuário recuperar a senha caso tenha esquecido,
     mediante verificação de email e resposta secreta.
     
     Parâmetros:
          repo (RepoUsuario): repositório que contém os usuários.
     """
     email = nao_vazio("Digite seu email cadastrado: ").lower()
     user = repo.buscar(email)
     
     if not user:
          print("Email não cadastrado!")
          return
     
     print("Responda a seguinte pergunta secreta cadastrada:")
     resposta_secreta = nao_vazio("Qual o nome da sua professora preferida? ")
     if resposta_secreta.lower() != user.resposta_secreta.lower():
          print("Resposta secreta incorreta!")
          return
     
     fluxo_alterar_senha(repo,email)
     print("Senha redefinida com sucesso! Você já pode fazer login com a nova senha.")

# Deletar usuario:
def deletar_conta(repo: RepoUsuario,email):
     """
     Exclui a conta do usuário após validação da senha e confirmação da intenção.

     Parâmetros:
          repo: instância de RepoUsuario que controla a persistência.
          email: email do usuário que deseja excluir a conta.

     Retorna:
          bool: True se a conta foi excluída com sucesso, False caso contrário.
     """
     senha = nao_vazio("Para excluir sua conta, confirme sua senha: ")
     user = repo.buscar(email)
     if senha == user.senha:
          confirmacao = nao_vazio("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
          if confirmacao != 's':
               print("Operação cancelada!")
               return False
     
     else:
          print("Senha incorreta! Retornando...")
          return False

     repo.remover(email)
     print("✔ Sua conta foi deletada com sucesso.")
     return True
