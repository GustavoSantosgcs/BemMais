from usuario import Usuario
from repo_usuario import RepoUsuario
from utils import nao_vazio, limpar_tela

class ServicoUsuario:
     
     def __init__(self, repo: RepoUsuario):
          self.repo = repo
          
          
     #Cadastro de usuário:
     def cadastrar_usuario(self):
          """
          Realiza o cadastro de um novo usuário com nome, telefone, email, senha e pergunta secreta.
          """ 
          limpar_tela()
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
                    if self.repo.buscar(email):   
                         print("Email já cadastrado!")
                         input("Pressione Enter para voltar ao inicio...")
                         return
                    else:
                         break    
                              
               while True:     
                    senha = nao_vazio("Digite uma senha com 6 digitos (apenas números): ")
                    if not Usuario.senha_valida(senha):
                         print("Senha inválida! Tente novamente.")
                         continue
                    confirmação = nao_vazio("Confirme a senha: ")
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
                    continue  
               
               try:
                    self.repo.cadastrar(novo)
                    print("✅ Cadastro realizado com sucesso!\n")
                    input("Pressione Enter para continuar...")
                    break
               except ValueError as msg_erro: # Verifica novamente se o email já é cadastrado
                    print(msg_erro)
                    

     # Fluxo de alteração de senha:     
     def alterar_senha_interativo(self, email): 
          """
          Fluxo para alterar a senha do usuário logado.
          Solicita a senha atual para autenticação, depois pede a nova senha e
          sua confirmação, valida o formato (6 dígitos) e persiste a mudança.

          Parâmetros:
               email (str): email do usuário que está logado.
          """
          limpar_tela()  
          user = self.repo.buscar(email)
          while True:
               nova_senha  = nao_vazio("Nova senha (6 dígitos numericos): ")
               confirmar_senha = nao_vazio("Confirme a nova senha: ")

               if nova_senha != confirmar_senha:
                    print("Senhas diferentes! Tente de novo.\n")
                    continue

               try:
                    user.alterar_senha(user.senha, nova_senha)   
                    self.repo.salvar_usuarios()            
                    print("Senha atualizada com sucesso!\n")
                    input("Pressione Enter para voltar…")    
                    limpar_tela()  
                    break
               except ValueError as msg_erro:
                    print(msg_erro)
                    input("Enter para tentar de novo…")
                    limpar_tela()


     # Fluxo de alteração de email:
     def alterar_email_interativo(self, email):
          """
          Fluxo de terminal para alterar o email de um usuário:

               1. Pede o novo email.
               2. Chama Usuario.alterar_email para validar.
               3. Persiste a mudança no repositório.
               4. Exibe mensagem de sucesso e retorna o email atualizado.
               
          Parâmetros:
               email (str): email atual do usuário logado.

          Retorna:
               str: o novo email em caso de sucesso, ou o email original em erro.
          """
          limpar_tela()
          novo_email = nao_vazio("Digite o novo email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
          if not Usuario.email_valido(novo_email):
               print("Formato de email inválido!")
               return email
          try:
               self.repo.atualizar_email(email, novo_email)
               print("✔  Seu email foi atualizado!")
               return novo_email
          
          except ValueError as erro:
               print("Erro: ",erro)
               return email


     # Fluxo de alteração da resposta secreta:
     def alterar_resposta_interativo(self, email):
          """
          Fluxo interativo de terminal para atualizar a resposta secreta de recuperação.
          Solicita confirmação de senha, pede a nova resposta secreta e persiste a mudança.
 
          Parâmetros:
               email (str): email do usuário que está logado.
          """
          limpar_tela()
          user = self.repo.buscar(email)
          senha = nao_vazio("Confirme sua senha atual: ")
          if senha != user.senha:
               print("Senha incorreta! Voltando ao menu...")
               return
          
          nova_resposta = nao_vazio("Digite a nova resposta secreta (professora favorita): ")
          try:
               user.alterar_resposta(nova_resposta)
               self.repo.salvar_usuarios()
               print("✔  Resposta secreta atualizada com sucesso!")
               
          except ValueError as erro:
               print("Erro: ",erro)

          
     # Editar usuario:
     def editar_conta(self,email):
          """
          Permite ao usuário logado editar suas informações pessoais.
          
          Parâmetros:
               email (str): email atual do usuário logado.
          Retorna:
               o email atualizado (ou o original, se não alterar).
          """
          limpar_tela()
          user = self.repo.buscar(email)
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
                         limpar_tela()
                         novo_email = self.alterar_email_interativo(email)
                         return novo_email     
                    case '2':
                         limpar_tela()
                         novo_nome = nao_vazio("Digite o novo nome: ").title()
                         user.nome = novo_nome
                         self.repo.salvar_usuarios()
                         print("✔ Nome atualizado com sucesso!")
                         
                    case '3':
                         limpar_tela()
                         novo_tel = nao_vazio("Digite o novo número de telefone com DDD Ex:(81) 99999-8888: ")
                         while not user.telefone_valido(novo_tel):
                              print("Formato inválido!")
                              novo_tel = nao_vazio("Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
                         
                         user.telefone = novo_tel
                         self.repo.salvar_usuarios()
                         print("✔ Telefone atualizado com sucesso!")
                         
                    case '4':
                         senha_atual = nao_vazio("Digite sua senha atual: ")
                         if senha_atual != user.senha:
                              print("🔒 Senha incorreta!")
                              input("Pressione Enter para voltar...")
                              limpar_tela()
                              continue
                         
                         self.alterar_senha_interativo(email)
                         continue
                                        
                    case '5':
                         self.alterar_resposta_interativo(email)
                    
                    case '0':
                         print("Vamos voltar então...\n")
                         break
                    
                    case _:
                         print("Opção inválida!")        
          return email


     # Recuperar senha:
     def recuperar_senha(self):
          """
          Permite ao usuário recuperar a senha caso tenha esquecido,
          mediante verificação de email e resposta secreta.
          
          Fluxo de recuperação de senha:
               1. Pede o email cadastrado.
               2. Verifica existência e pergunta secreta.
               3. Chama fluxo de alteração de senha.
          """
          limpar_tela()
          email = nao_vazio("Digite seu email cadastrado: ").lower()
          user = self.repo.buscar(email)
          
          if not user:
               print("Email não cadastrado!")
               return
          
          print("\nResponda a seguinte pergunta secreta cadastrada:")
          resposta_secreta = nao_vazio("Qual o nome da sua professora preferida? ")
          if resposta_secreta.lower() != user.resposta_secreta.lower():
               print("Resposta secreta incorreta!")
               return
          
          self.alterar_senha_interativo(email)
          print("Senha redefinida com sucesso! Você já pode fazer login com a nova senha.")

     # Deletar usuario:
     def deletar_conta(self,email):
          """
          Exclui a conta do usuário após validação da senha e confirmação da intenção.

          Parâmetros:
               email: email do usuário que deseja excluir a conta.

          Retorna:
               bool: True se a conta foi excluída com sucesso, False caso contrário.
          """
          limpar_tela()
          senha = nao_vazio("Para excluir sua conta, confirme sua senha: ")
          user = self.repo.buscar(email)
          if senha == user.senha:
               confirmacao = nao_vazio("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
               if confirmacao != 's':
                    print("Operação cancelada!")
                    return False
          
          else:
               print("Senha incorreta! Retornando...")
               return False

          self.repo.remover(email)
          print("✔ Sua conta foi deletada com sucesso.")
          return True
