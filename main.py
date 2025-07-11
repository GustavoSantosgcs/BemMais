from repo_usuario import RepoUsuario
from serv_usuario import ServicoUsuario
from utils import Utils
from frases import FraseDia
from dilema import Dilema
from desafios import DesafioBem, ListaDesafios, RepoVoucher


class BemMais:
     """
     Aplicação BEM+ que gerencia cadastro, login, menus e integra serviços.
     """
     def __init__(self):
          """
          Aplicação BEM+ que orquestra todos os módulos do sistema.

          Nesta inicialização são configurados:
               - repo_user: repositório de usuários (persistência em JSON).
               - serv_user: serviço de fluxo interativo de usuário (cadastro, edição, etc.).
               - dilema: módulo de cenários éticos, carregando perguntas de arquivo JSON.
               - serv_frase: serviço responsável por gerenciar a Frase do Dia.
               - desafios: módulo de “Desafios do Bem”, com desafios regulares e premium (com voucher).
          """
          self.repo_user = RepoUsuario()
          self.serv_user = ServicoUsuario(self.repo_user)
          desafios_repo = ListaDesafios()
          voucher_repo = RepoVoucher()
          self.dilema = Dilema(self.repo_user)
          self.serv_frase = FraseDia()
          self.desafios = DesafioBem(self.repo_user, desafios_repo, voucher_repo)


     #Ver pontuação e nível:
     def pontuacaoENivel(self, email):
          """
          Exibe, com uma saudação personalizada, a pontuação e
          o nível do usuário com base nos pontos acumulados.

          Parâmetros:
               email (str): email do usuário cujo progresso será exibido.
          """
          user = self.repo_user.buscar(email)

          if user.pontos < 10:
               nivel = 'Iniciante 🐣'
          elif user.pontos < 40:
               nivel = 'Explorador 🌱'
          elif user.pontos < 70:
               nivel = 'Consciente 💡'
          elif user.pontos < 90:
               nivel = 'Mentor 🌟'
          else:
               nivel = 'Mestre 👑'
               
          Utils.limparTela()     
          print(f"\n🚀 Olá, {user.nome}! Sua jornada pelo BEM+ está em andamento.")
          print("Vamos conferir seu progresso e o impacto positivo que você está construindo...\n")
          print(f"\n⭐ Pontuação total: {user.pontos} pontos")
          print(f"🔰 Nível atual: {nivel}\n")


     # Ranking de Usuários:
     def rankingUsuarios(self):
          """
          Exibe um ranking dos cinco usuários com maior pontuação.

          Parâmetros:
               repo (RepoUsuario): repositório de usuários.    
          """
          users = self.repo_user.listar()
          
          # Ordena direto as instâncias pelo atributo 'pontos'
          top5 = sorted(users, key=lambda user: user.pontos, reverse=True)[:5]
          
          Utils.limparTela()
          print("\n🏆 Top 5 Usuários 🏆\n")
          print(f"{'Pos':<3} {'Nome':<20} {'Pontos':>6}")
          print("=" * 31)

          # Linhas do ranking
          for pos, user in enumerate(top5, 1):
               print(f"{pos:<3} {user.nome:<20} {user.pontos:>6}")

          print("=" * 31)
          
          
     # Histórico de Respostas do usuário:
     def exibirHistorico(self,email):
          """
          Exibe o histórico de respostas do usuário aos cenários éticos, quando existir.
          
          Parâmetros:
               email (str): email do usuário cujo histórico será exibido.
          """     
          user = self.repo_user.buscar(email)
          Utils.limparTela()
          historico = user.historico_respostas
          if not historico:
               print("\n🤔 Você ainda não realizou nenhum cenário ético.")
          else:
               print("\n📃 Histórico de Respostas\n")
               for i, chave in enumerate(historico, 1):
                    print(f"{i}. [{chave['data']}] Pergunta: {chave['pergunta']}")
                    print(f"   Sua resposta: ({chave['resposta']}) — +{chave['pontos']} ponto(s)\n")

          
     # Menu do usuário:
     def login(self):
          """
          Realiza o login de um usuário e apresenta opções para acessar o menu BEM+,
          editar conta, deletar conta ou sair.
          """
          email = Utils.naoVazio("Digite seu email: ").lower()
          senha = input("Digite sua senha: ")
          user = self.repo_user.buscar(email)
          if not (user and user.senha == senha):
               print("Email ou senha inválidos. ")
               input ("Pressione ENTER para voltar...")
               return
          
          while True:
               Utils.limparTela()
               print(f"\nBem-vindo(a), {user.nome}")
               print("O que deseja fazer? ")
               print("1 - Prosseguir para o Menu BEM+")
               print("2 - Editar Conta")
               print("3 - Deletar Conta")
               print("0 - Sair")
               op = input("Opção: ")
               match op:
                    case '1':
                         print("Então vamos continuar! ")
                         self.menuBem(email)
                    case '2':
                         email = self.serv_user.editarConta(email)
                    case '3':
                         if self.serv_user.deletarConta(email):
                              break
                    case '0':
                         print("Até mais então...")
                         break
                    case _:
                         print("opção inválida")          
                         input("Pressione Enter para continuar…")
                         Utils.limparTela()


     # Menu BEM+:
     def menuBem(self,email):
          """
          Apresenta o menu principal do BEM+ com as opções de funcionalidades ao usuário.

          Parâmetros:
               email (str): email do usuário logado.
          """    
          while True:
               Utils.limparTela()
               user = self.repo_user.buscar(email) 
               print("\n" + "="*38)
               print(f"🌟 MENU BEM+ - {user.nome} 🌟".center(38))
               print("="*38)
               print("│ 1 - Frase do Dia                  │")
               print("│ 2 - Iniciar Cenário Ético         │")
               print("│ 3 - Desafios do Bem               │")
               print("│ 4 - Ver Pontuação e Nível         │")
               print("│ 5 - Ranking de Usuários           │")
               print("│ 6 - Ver Histórico de Respostas    │")
               print("│ 0 - Sair do menu BEM+             │")
               print("="*38)          
               opcao_bem = input("Sua opção é? ")
               match opcao_bem:
                    case '1':
                         self.serv_frase.fraseDia()
                         input("\nPressione Enter para continuar...")
                    
                    case '2':
                         pontos = self.dilema.executarDilema(email)
                         user.pontos += pontos
                         self.repo_user.salvarUsuarios()
                         
                    case '3':
                         self.desafios.desafiosBem(email)
                         
                    case '4':
                         self.pontuacaoENivel(email)
                         input("\nPressione Enter para continuar...")
                    
                    case '5':
                         self.rankingUsuarios()
                         input("\nPressione Enter para continuar...")
                    
                    case '6':
                         self.exibirHistorico(email)
                         input("\nPressione Enter para continuar...")
                    
                    case '0':
                         print("Saindo do Menu BEM+...")
                         input("\nPressione Enter para retornar...")
                         return
                    
                    case _:
                         print("Opção invalida!")   
                         input("Pressione Enter para continuar…")
                         Utils.limparTela()    

               
     # Menu inicial:
     def menuInicial(self):
          """
          Exibe o menu inicial de cadastro, login e recuperação de senha.
         """     
          while True:
               Utils.limparTela()
               print("\n" + "="*32)
               print("📘  MENU INICIAL - BEM+  📘".center(32))
               print("="*32)
               print("│ 1 - Cadastrar               │")
               print("│ 2 - Login                   │")
               print("│ 3 - Recuperação de senha    │")
               print("│ 0 - Sair                    │")
               print("="*32)
               opcao = input("Escolha uma opção: ")
               
               match opcao:
                    case '1':
                         self.serv_user.cadastrarUsuario()
                    case '2':
                         self.login()
                    case '3':
                         self.serv_user.recuperarSenha()
                    case '0':
                         print("Até mais então...")
                         break
                    case _:
                         print("opção inválida") 
                         input("Pressione Enter para continuar…")
                         Utils.limparTela()                 


# Main:
if __name__ == "__main__":
     app = BemMais()
     app.menuInicial()