from repo_usuario import RepoUsuario
from serv_usuario import ServicoUsuario
from utils import nao_vazio, limpar_tela
from frases import frase_dia
from dilema import iniciar_dilema
from desafios import desafios_bem


#Ver pontuação e nível:
def pontuacao_e_nivel(repo: RepoUsuario, email):
     """
     Exibe, com uma saudação personalizada, a pontuação e
     o nível do usuário com base nos pontos acumulados.

     Parâmetros:
          repo (RepoUsuario): repositório de usuários persistido em JSON.
          email (str): email do usuário cujo progresso será exibido.
     """
     user = repo.buscar(email)

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
          
     limpar_tela()     
     print(f"\n🚀 Olá, {user.nome}! Sua jornada pelo BEM+ está em andamento.")
     print("Vamos conferir seu progresso e o impacto positivo que você está construindo...\n")
     print(f"\n⭐ Pontuação total: {user.pontos} pontos")
     print(f"🔰 Nível atual: {nivel}\n")


# Ranking de Usuários:
def ranking_usuarios(repo: RepoUsuario):
     """
     Exibe um ranking dos cinco usuários com maior pontuação.

     Parâmetros:
          repo (RepoUsuario): repositório de usuários.    
     """
     users = repo.listar()
     
     # Ordena direto as instâncias pelo atributo 'pontos'
     top5 = sorted(users, key=lambda user: user.pontos, reverse=True)[:5]
     
     limpar_tela()
     print("\n🏆 Top 5 Usuários 🏆\n")
     print(f"{'Pos':<3} {'Nome':<20} {'Pontos':>6}")
     print("=" * 31)

     # Linhas do ranking
     for pos, user in enumerate(top5, 1):
          print(f"{pos:<3} {user.nome:<20} {user.pontos:>6}")

     print("=" * 31)
     
     
# Histórico de Respostas do usuário:
def exibir_historico(repo: RepoUsuario,email):
     """
     Exibe o histórico de respostas do usuário aos cenários éticos, quando existir.
     
     Parâmetros:
          repo (RepoUsuario): repositório de usuários persistido em JSON.
          email (str): email do usuário cujo histórico será exibido.
     """     
     user = repo.buscar(email)
     limpar_tela()
     historico = user.historico_respostas
     if not historico:
          print("\n🤔 Você ainda não realizou nenhum cenário ético.")
     else:
          print("\n📃 Histórico de Respostas\n")
          for i, chave in enumerate(historico, 1):
               print(f"{i}. [{chave['data']}] Pergunta: {chave['pergunta']}")
               print(f"   Sua resposta: ({chave['resposta']}) — +{chave['pontos']} ponto(s)\n")

     
# Menu do usuário:
def login(repo: RepoUsuario, serv: ServicoUsuario):
     """
     Realiza o login de um usuário e apresenta opções para acessar o menu BEM+,
     editar conta, deletar conta ou sair.

     Parâmetros:
          repo (RepoUsuario): repositório de usuários persistido em JSON.
     """
     email = nao_vazio("Digite seu email: ").lower()
     senha = input("Digite sua senha: ")
     user = repo.buscar(email)
     if not (user and user.senha == senha):
          print("Email ou senha inválidos. ")
          return
     
     while True:
          limpar_tela()
          print(f"\nBem-vindo(a), {user.nome}")
          print("O que deseja fazer? ")
          print("1 - Prosseguir para o Menu BEM+")
          print("2 - Editar Conta")
          print("3 - Deletar Conta")
          print("4 - Sair")
          op = input("Opção: ")
          match op:
               case '1':
                    print("Então vamos continuar! ")
                    menu_bem(repo,email)
               case '2':
                    email = serv.editar_conta(email)
               case '3':
                    if serv.deletar_conta(email):
                         break
               case '4':
                    print("Até mais então...")
                    break
               case _:
                    print("opção inválida")          
                    input("Pressione Enter para continuar…")
                    limpar_tela()


# Menu BEM+:
def menu_bem(repo: RepoUsuario,email):
     """
     Apresenta o menu principal do BEM+ com as opções de funcionalidades ao usuário.

     Parâmetros:
          repo (RepoUsuario): repositório de usuários persistido em JSON.
          email (str): email do usuário logado.
     """    
     user = repo.buscar(email) 
     while True:
          limpar_tela()
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
                    frase_dia()
                    input("\nPressione Enter para continuar...")
               
               case '2':
                    pontos = iniciar_dilema(repo,email)
                    user.pontos += pontos
                    repo.salvar_usuarios()
                    
               case '3':
                    desafios_bem(repo,email)
                    
               case '4':
                    pontuacao_e_nivel(repo,email)
                    input("\nPressione Enter para continuar...")
               
               case '5':
                    ranking_usuarios(repo)
                    input("\nPressione Enter para continuar...")
               
               case '6':
                    exibir_historico(repo, email)
                    input("\nPressione Enter para continuar...")
               
               case '0':
                    print("Saindo do Menu BEM+...")
                    input("\nPressione Enter para retornar...")
                    return
               
               case _:
                    print("Opção invalida!")   
                    input("Pressione Enter para continuar…")
                    limpar_tela()    

          
# Menu inicial:
def menu_inicial(repo: RepoUsuario, serv: ServicoUsuario):
     """
     Exibe o menu inicial de cadastro, login e recuperação de senha.

     Parâmetros:
          repo (RepoUsuario): repositório de usuários persistido em JSON.
     """     
     while True:
          limpar_tela()
          print("\n" + "="*32)
          print("📘  MENU INICIAL - BEM+  📘".center(32))
          print("="*32)
          print("│ 1 - Cadastrar               │")
          print("│ 2 - Login                   │")
          print("│ 3 - Recuperação de senha    │")
          print("│ 4 - Sair                    │")
          print("="*32)
          opcao = input("Escolha uma opção: ")
             
          match opcao:
               case '1':
                    serv.cadastrar_usuario()
               case '2':
                    login(repo, serv)
               case '3':
                    serv.recuperar_senha()
               case '4':
                    print("Até mais então...")
                    break
               case _:
                    print("opção inválida") 
                    input("Pressione Enter para continuar…")
                    limpar_tela()                 


# Main:
if __name__ == "__main__":
     repo = RepoUsuario()
     serv = ServicoUsuario(repo)
     menu_inicial(repo, serv)