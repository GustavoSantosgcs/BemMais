from usuario import Usuario
from repo_usuario import RepoUsuario
from utils import Utils

class ServicoUsuario:
     
     def __init__(self, repo: RepoUsuario):
          self.repo = repo
          
          
     #Cadastro de usuário:
     def cadastrarUsuario(self):
          """
          Realiza o cadastro de um novo usuário com nome, telefone, email, senha e pergunta secreta.
          """ 
          Utils.limparTela()
          while True: # looping externo de cadastro
               nome = Utils.naoVazio("Digite seu nome de usuário: ").title()
               telefone = Utils.naoVazio("Digite seu telefone com DDD Ex:(81) 9xxxx-xxxx: ")
               while not Usuario.telefoneValido(telefone):
                    print("Erro de digitação!")
                    telefone = Utils.naoVazio(" Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
               
               while True:  
                    email = Utils.naoVazio("Digite seu email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
                    if not Usuario.emailValido(email):
                         print("Formato de email inválido!")
                         continue
                    if self.repo.buscar(email):   
                         print("Email já cadastrado!")
                         input("Pressione Enter para voltar ao inicio...")
                         return
                    else:
                         break    
                              
               while True:     
                    senha = Utils.naoVazio("Digite uma senha com 6 digitos (apenas números): ")
                    if not Usuario.senhaValida(senha):
                         print("Senha inválida! Tente novamente.")
                         continue
                    confirmação = Utils.naoVazio("Confirme a senha: ")
                    if confirmação == senha:
                         print("Perfeito! Senhas iguais.")
                         break
                    else:
                         print("Senhas diferentes! Tente novamente...")
                    
               print("\nPara recuperação de senha, responda a seguinte pergunta: ")   
               resposta_secreta = Utils.naoVazio("Qual o nome do seu(a) professor(a) favorito(a)? ")
                    
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
     def alterarSenhaInterativo(self, email): 
          """
          Fluxo para alterar a senha do usuário logado.
          Solicita a senha atual para autenticação, depois pede a nova senha e
          sua confirmação, valida o formato (6 dígitos) e persiste a mudança.

          Parâmetros:
               email (str): email do usuário que está logado.
          """
          Utils.limparTela()  
          user = self.repo.buscar(email)
          while True:
               nova_senha  = Utils.naoVazio("Nova senha (6 dígitos numericos): ")
               confirmar_senha = Utils.naoVazio("Confirme a nova senha: ")

               if nova_senha != confirmar_senha:
                    print("Senhas diferentes! Tente de novo.\n")
                    continue

               try:
                    user.alterarSenha(user.senha, nova_senha)   
                    self.repo.salvarUsuarios()            
                    print("Senha atualizada com sucesso!\n")
                    input("Pressione Enter para voltar…")    
                    Utils.limparTela()  
                    break
               except ValueError as msg_erro:
                    print(msg_erro)
                    input("Enter para tentar de novo…")
                    Utils.limparTela()


     # Fluxo de alteração de email:
     def alterarEmailInterativo(self, email):
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
          Utils.limparTela()
          novo_email = Utils.naoVazio("Digite o novo email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
          if not Usuario.emailValido(novo_email):
               print("Formato de email inválido!")
               return email
          try:
               self.repo.atualizarEmail(email, novo_email)
               print("✔  Seu email foi atualizado!")
               return novo_email
          
          except ValueError as erro:
               print("Erro: ",erro)
               return email


     # Fluxo de alteração da resposta secreta:
     def alterarRespostaInterativo(self, email):
          """
          Fluxo interativo de terminal para atualizar a resposta secreta de recuperação.
          Solicita confirmação de senha, pede a nova resposta secreta e persiste a mudança.
 
          Parâmetros:
               email (str): email do usuário que está logado.
          """
          Utils.limparTela()
          user = self.repo.buscar(email)
          senha = Utils.naoVazio("Confirme sua senha atual: ")
          if senha != user.senha:
               print("Senha incorreta! Voltando ao menu...")
               return
          
          nova_resposta = Utils.naoVazio("Digite a nova resposta secreta (professora favorita): ")
          try:
               user.alterarResposta(nova_resposta)
               self.repo.salvarUsuarios()
               print("✔  Resposta secreta atualizada com sucesso!")
               
          except ValueError as erro:
               print("Erro: ",erro)

          
     # Editar usuario:
     def editarConta(self,email):
          """
          Permite ao usuário logado editar suas informações pessoais.
          
          Parâmetros:
               email (str): email atual do usuário logado.
          Retorna:
               o email atualizado (ou o original, se não alterar).
          """
          Utils.limparTela()
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
                         Utils.limparTela()
                         novo_email = self.alterarEmailInterativo(email)
                         return novo_email     
                    case '2':
                         Utils.limparTela()
                         novo_nome = Utils.naoVazio("Digite o novo nome: ").title()
                         user.nome = novo_nome
                         self.repo.salvarUsuarios()
                         print("✔ Nome atualizado com sucesso!")
                         
                    case '3':
                         Utils.limparTela()
                         novo_tel = Utils.naoVazio("Digite o novo número de telefone com DDD Ex:(81) 99999-8888: ")
                         while not user.telefoneValido(novo_tel):
                              print("Formato inválido!")
                              novo_tel = Utils.naoVazio("Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
                         
                         user.telefone = novo_tel
                         self.repo.salvarUsuarios()
                         print("✔ Telefone atualizado com sucesso!")
                         
                    case '4':
                         senha_atual = Utils.naoVazio("Digite sua senha atual: ")
                         if senha_atual != user.senha:
                              print("🔒 Senha incorreta!")
                              input("Pressione Enter para voltar...")
                              Utils.limparTela()
                              continue
                         
                         self.alterarSenhaInterativo(email)
                         continue
                                        
                    case '5':
                         self.alterarRespostaInterativo(email)
                    
                    case '0':
                         print("Vamos voltar então...\n")
                         break
                    
                    case _:
                         print("Opção inválida!")        
          return email


     # Recuperar senha:
     def recuperarSenha(self):
          """
          Permite ao usuário recuperar a senha caso tenha esquecido,
          mediante verificação de email e resposta secreta.
          
          Fluxo de recuperação de senha:
               1. Pede o email cadastrado.
               2. Verifica existência e pergunta secreta.
               3. Chama fluxo de alteração de senha.
          """
          Utils.limparTela()
          email = Utils.naoVazio("Digite seu email cadastrado: ").lower()
          user = self.repo.buscar(email)
          
          if not user:
               print("Email não cadastrado!")
               return
          
          print("\nResponda a seguinte pergunta secreta cadastrada:")
          resposta_secreta = Utils.naoVazio("Qual o nome da sua professora preferida? ")
          if resposta_secreta.lower() != user.resposta_secreta.lower():
               print("Resposta secreta incorreta!")
               return
          
          self.alterarSenhaInterativo(email)
          print("Senha redefinida com sucesso! Você já pode fazer login com a nova senha.")

     # Deletar usuario:
     def deletarConta(self,email):
          """
          Exclui a conta do usuário após validação da senha e confirmação da intenção.

          Parâmetros:
               email: email do usuário que deseja excluir a conta.

          Retorna:
               bool: True se a conta foi excluída com sucesso, False caso contrário.
          """
          Utils.limparTela()
          senha = Utils.naoVazio("Para excluir sua conta, confirme sua senha: ")
          user = self.repo.buscar(email)
          if senha == user.senha:
               confirmacao = Utils.naoVazio("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
               if confirmacao != 's':
                    print("Operação cancelada!")
                    return False
          
          else:
               print("Senha incorreta! Retornando...")
               return False

          self.repo.remover(email)
          print("✔ Sua conta foi deletada com sucesso.")
          return True
