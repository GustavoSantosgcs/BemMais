from .usuario import Usuario
from .repo_usuario import RepoUsuario
from .utils import Utils
from .ui import Ui


class ServicoUsuario:
     """
     Lida com as interações interativas do usuário: cadastro, edição,
     alteração de dados e recuperação de senha.
     """
     
     def __init__(self, repo: RepoUsuario, ui: Ui):
          """
          Inicializa o serviço de usuário com repositório e interface.

          Args:
               repo (RepoUsuario): Repositório para persistência dos usuários.
               ui (Ui): Interface para exibição e interação com o terminal.
          """
          
          self.repo = repo
          self.ui = ui
      
     def cadastrarUsuario(self):
          """
          Realiza o cadastro interativo de um novo usuário.

          O fluxo valida telefone, email e senha, coleta resposta secreta e persiste o novo usuário.
          """
          
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
                         self.ui.pausar()
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
                    self.ui.pausar()
                    continue  
               
               self.repo.cadastrar(novo)
               print("✅ Cadastro realizado com sucesso!\n")
               self.ui.pausar()
               break

     # Fluxo de alteração de senha:     
     def alterarSenhaInterativo(self, email): 
          """
          Fluxo para alterar a senha do usuário logado.
         Solicita a nova senha e confirmação, valida e atualiza a senha no repositório.

          Args:
               email (str): Email do usuário logado.
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
                    self.ui.pausar()    
                    Utils.limparTela()  
                    break
               except ValueError as msg_erro:
                    print(msg_erro)
                    self.ui.pausar()
                    Utils.limparTela()

     # Fluxo de alteração de email:
     def alterarEmailInterativo(self, email):
          """
          Altera o email do usuário após validação.

          Args:
               email (str): Email atual do usuário.

          Returns:
               str: Novo email em caso de sucesso, ou o original se houver erro.
          """
          Utils.limparTela()
          novo_email = Utils.naoVazio("Digite o novo email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
          if not Usuario.emailValido(novo_email):
               print("Formato de email inválido!")
               self.ui.pausar()
               return email
          try:
               self.repo.atualizarEmail(email, novo_email)
               print("✔  Seu email foi atualizado!")
               self.ui.pausar()
               return novo_email
          
          except ValueError as erro:
               print("Erro: ",erro)
               self.ui.pausar()
               return email

     # Fluxo de alteração da resposta secreta:
     def alterarRespostaInterativo(self, email):
          """
          Altera a resposta secreta do usuário, após confirmação de senha.

          Args:
               email (str): Email do usuário logado.
          """
          Utils.limparTela()
          user = self.repo.buscar(email)
          senha = Utils.naoVazio("Confirme sua senha atual: ")
          if senha != user.senha:
               print("Senha incorreta! Voltaremos ao menu")
               self.ui.pausar()
               return
          
          nova_resposta = Utils.naoVazio("Digite a nova resposta secreta (professor(a) favorito(a)): ")
          try:
               user.alterarResposta(nova_resposta)
               self.repo.salvarUsuarios()
               print("✔  Resposta secreta atualizada com sucesso!")
               self.ui.pausar()
               
          except ValueError as erro:
               print("Erro: ",erro)
               self.ui.pausar()

     def editarConta(self,email):
          """
          Menu interativo para edição de dados da conta.
          Permite alterar nome, telefone, senha, email ou pergunta secreta.

          Args:
               email (str): Email atual do usuário.

          Returns:
               str: Novo email, ou original se não for alterado.
          """
          Utils.limparTela()
          user = self.repo.buscar(email)
          while True:
               self.ui.tituloDaFuncRich("Editar Conta", cor="cyan")

               # Mostra dados atuais
               self.ui.console.print(f"[bold]Email:[/bold] {user.email}")
               self.ui.console.print(f"[bold]Nome :[/bold] {user.nome}")
               self.ui.console.print(f"[bold]Telefone:[/bold] {user.telefone}\n")

               # Menu de opções de edição
               itens = [
                    ("1", "Email"),
                    ("2", "Nome"),
                    ("3", "Telefone"),
                    ("4", "Senha"),
                    ("5", "Pergunta Secreta"),
                    ("0", "Voltar")
               ]
               self.ui.showMenu("O que deseja editar?", itens, cor="cyan", limpar_tela=False)
               opcao = self.ui.console.input("\n[bold]Opção:[/bold] ").strip()

               match opcao:
                    case '1': 
                         novo_email = self.alterarEmailInterativo(email)
                         return novo_email
                         
                    case '2':
                         novo_nome = Utils.naoVazio("Digite o novo nome: ").title()
                         user.nome = novo_nome
                         self.repo.salvarUsuarios()
                         print("✔ Nome atualizado com sucesso!")
                         self.ui.pausar()
                         
                    case '3':
                         novo_tel = Utils.naoVazio("Digite o novo número de telefone com DDD Ex:(81) 99999-8888: ")
                         while not user.telefoneValido(novo_tel):
                              print("Formato inválido!")
                              novo_tel = Utils.naoVazio("Tente novamente conforme exemplo (xx) 9xxxx-xxxx: ")
                              
                         user.telefone = novo_tel
                         self.repo.salvarUsuarios()
                         print("✔ Telefone atualizado com sucesso!")
                         self.ui.pausar()
                         
                    case '4':
                         senha_atual = Utils.naoVazio("Digite sua senha atual: ")
                         if senha_atual != user.senha:
                              print("🔒 Senha incorreta!")
                              self.ui.pausar()
                              Utils.limparTela()
                              continue
                         
                         self.alterarSenhaInterativo(email)
                         continue
                                        
                    case '5':
                         self.alterarRespostaInterativo(email)
                    
                    case '0':
                         print("OK! Vamos voltar então.\n")
                         self.ui.pausar()
                         break
                    
                    case _:
                         print("Opção inválida!")        
          return email

     def recuperarSenha(self):
          """
          Recupera a senha de um usuário após validação do email e da resposta secreta.

          Exibe um fluxo interativo com verificação e redirecionamento para alteração de senha.
          """
          
          self.ui.tituloDaFuncRich("Recuperar Senha", cor="blue")
          email = Utils.naoVazio("Digite seu email cadastrado: ").lower()
          user = self.repo.buscar(email)
          
          if not user:
               print("Email não cadastrado!")
               self.ui.pausar()
               return
          
          print("\nResponda a seguinte pergunta secreta cadastrada:")
          resposta_secreta = Utils.naoVazio("Qual o nome do(a) seu(sua) professor(a) preferido(a)? ")
          if resposta_secreta.lower() != user.resposta_secreta.lower():
               print("Resposta secreta incorreta!")
               self.ui.pausar()
               return
          
          self.alterarSenhaInterativo(email)
          print("Senha redefinida com sucesso! Você já pode fazer login com a nova senha. 😉")
          self.ui.pausar()

     # Deletar usuario:
     def deletarConta(self,email):
          """
          Exclui a conta do usuário após validação de senha e confirmação.

          Args:
               email (str): Email do usuário que deseja excluir a conta.

          Returns:
               bool: True se a conta foi excluída com sucesso, False caso contrário.
          """
          Utils.limparTela()
          self.ui.tituloDaFuncRich("Deletar Conta", cor="red")
          senha = Utils.naoVazio("Para excluir sua conta, confirme sua senha: ")
          user = self.repo.buscar(email)
          
          if senha == user.senha:
               confirmacao = Utils.naoVazio("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
               if confirmacao != 's':
                    print("Operação cancelada!")
                    self.ui.pausar()
                    return False
          
          else:
               print("Senha incorreta! Retornando...")
               self.ui.pausar()
               return False

          self.repo.remover(email)
          print("✔ Sua conta foi deletada com sucesso.")
          self.ui.pausar()
          return True
