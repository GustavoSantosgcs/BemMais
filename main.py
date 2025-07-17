from app.repo_usuario import RepoUsuario
from app.serv_usuario import ServicoUsuario
from app.utils import Utils
from app.frases import FraseDia
from app.dilema import Dilema
from app.desafios import DesafioBem, ListaDesafios, RepoVoucher
from app.ui import Ui
from rich.table import Table
from rich import box


class BemMais:
     """
     Classe principal da aplicação BEM+.

     Responsável por orquestrar os módulos do sistema:
     cadastro, login, menus, dilemas éticos, desafios, pontuação e ranking.
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
          self.ui = Ui()
          self.repo_user = RepoUsuario()
          self.serv_user = ServicoUsuario(self.repo_user, self.ui)
          desafios_repo = ListaDesafios()
          voucher_repo = RepoVoucher()
          self.dilema = Dilema(self.repo_user)
          self.serv_frase = FraseDia(self.ui)
          self.desafios = DesafioBem(self.repo_user, desafios_repo, voucher_repo, self.ui)

     def pontuacaoENivel(self, email):
          """
          Exibe, com uma saudação personalizada, a pontuação e
          o nível do usuário com base nos pontos acumulados.

          Args:
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
          self.ui.tituloDaFuncRich("Pontuação e Nível", cor="cyan")   
          saudacao = f"🚀 Olá, {user.nome}! Sua jornada pelo BEM+ está em andamento."
          self.ui.escrever(saudacao, delay=0.01)
          tabela = Table(box=None, show_header=False, padding=(0,1))
          tabela.add_column("Métrica", style="bold cyan")
          tabela.add_column("Valor", style="white")
          tabela.add_row("⭐ Pontuação total", f"{user.pontos} pontos")
          tabela.add_row("🔰 Nível atual", nivel)
          self.ui.console.print(tabela)

     def rankingUsuarios(self):
          """
          Exibe um Ranking do top cinco usuários com maior pontuação,
          em um layout Rich com medalhas para os 3 melhores colocados.
          
          Args:
               email (str): Email do usuário.
          """
          
          # Busca e ordena os usuários
          users = sorted(
               self.repo_user.listar(),
               key=lambda u: u.pontos,
               reverse=True
          )[:5]
          
          self.ui.tituloDaFuncRich("🏆 Ranking de Usuários 🏆", cor="gold1")

          # Tabela Rich
          tabela = Table(
               show_header=True,
               header_style="bold magenta",
               box=None,
               padding=(0,1),
          )
          tabela.add_column("Pos", justify="center", style="cyan")
          tabela.add_column("Nome", style="green")
          tabela.add_column("Pontos", justify="right", style="yellow")

          # Medalhas para os 3 primeiros
          medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}

          for pos, user in enumerate(users, start=1):
               medalha = medalhas.get(pos, " ")
               # dá negrito aos três primeiros
               row_style = "bold" if pos <= 3 else ""
               tabela.add_row(
                    f"{medalha} {pos}",
                    user.nome,
                    str(user.pontos),
                    style=row_style
               )

          self.ui.console.print(tabela)    
          
     # Histórico de Respostas do usuário:
     def exibirHistorico(self,email):
          """
          Exibe o histórico de respostas do usuário aos cenários éticos, quando existir.
          
          Args:
               email (str): email do usuário cujo histórico será exibido.
          """     
          user = self.repo_user.buscar(email)
          Utils.limparTela()
          historico = user.historico_respostas
          self.ui.tituloDaFuncRich("📃 Histórico de Respostas 📃", cor="purple")
          
          if not historico:
               self.ui.console.print("\n[yellow]🤔 Você ainda não realizou nenhum cenário ético.[/yellow]")
               return
          
          else:
               tabela = Table(
                title="Sua Jornada de Reflexões",
                box=box.ROUNDED,
                header_style="bold purple",
                border_style="purple",
                show_lines=True
            )
          tabela.add_column("Data", style="cyan", justify="center", width=12)
          tabela.add_column("Pergunta do Cenário", style="white", min_width=30, ratio=1)
          tabela.add_column("Sua Resposta", style="green", justify="center")
          tabela.add_column("Pontos", style="yellow", justify="right")
          
          for item in historico:
               tabela.add_row(
                    item["data"],
                    item["pergunta"],
                    f"[bold]{item['resposta_key']}[/bold] – {item['texto_resposta']}",
                    f"+{item['pontos']}"
               )
            
          self.ui.console.print(tabela)
      
     # Menu do usuário logado:
     def login(self):
          """
          Apresenta o menu principal do BEM+ com todas as funcionalidades disponíveis.

          Args:
               email (str): Email do usuário logado.
          """
          email = Utils.naoVazio("Digite seu email: ").lower()
          senha = Utils.naoVazio("Digite sua senha: ")
          user = self.repo_user.buscar(email)
          if not (user and user.senha == senha):
               print("Email ou senha inválidos. ")
               self.ui.pausar()
               return
          
          while True:
               Utils.limparTela()
               self.ui.tituloDaFuncRich(f"Bem-vindo, {user.nome}", cor="blue")
               
               itens = [
                    ("1", "Prosseguir para o Menu BEM+"),
                    ("2", "Editar Conta"),
                    ("3", "Deletar Conta"),
                    ("0", "Sair"),
               ]
               self.ui.showMenu("Opções de Conta", itens, cor="blue")

               opcao = self.ui.console.input("\n[bold]Opção:[/bold] ").strip()
               match opcao:
                    case '1':
                         print("Então vamos continuar! ")
                         self.menuBem(email)
                    case '2':
                         email = self.serv_user.editarConta(email)
                    case '3':
                         if self.serv_user.deletarConta(email):
                              return
                    case '0':
                         print("Ok! Até logo...")
                         return
                    case _:
                         self.ui.console.print("[red]Opção inválida![/red]")          
                         self.ui.pausar()
                         Utils.limparTela()

     # Menu BEM+:
     def menuBem(self,email):
          """
          Apresenta o menu principal do BEM+ com as opções de funcionalidades ao usuário.

          Args:
               email (str): email do usuário logado.
          """    
          while True:
               Utils.limparTela()
               user = self.repo_user.buscar(email) 
               opcao_bem  = self.ui.menuBemRich(user.nome)
               
               match opcao_bem:
                    case '1':
                         self.serv_frase.fraseDia()
                         self.ui.pausar()
                    
                    case '2':
                         pontos = self.dilema.executarDilema(email)
                         user.pontos += pontos
                         self.repo_user.salvarUsuarios()
                         
                    case '3':
                         self.desafios.desafiosBem(email)
                         
                    case '4':
                         self.pontuacaoENivel(email)
                         self.ui.pausar()
                    
                    case '5':
                         self.rankingUsuarios()
                         self.ui.pausar()
                    
                    case '6':
                         self.exibirHistorico(email)
                         self.ui.pausar()
                    
                    case '0':
                         print("Saindo do Menu BEM+...")
                         self.ui.pausar()
                         return
                    
                    case _:
                         print("Opção invalida!")   
                         self.ui.pausar()
                         Utils.limparTela()    
        
     def menuInicial(self):
          """
          Exibe o menu inicial de cadastro, login e recuperação de senha.
         """     
          while True:
               opcao = self.ui.menuInicialRich()
               
               match opcao:
                    case '1':
                         Utils.limparTela()
                         self.ui.tituloDaFuncRich("Cadastro de Usuário", cor="magenta")
                         self.serv_user.cadastrarUsuario()
                         
                    case '2':
                         self.ui.tituloDaFuncRich("Login", cor="yellow")
                         self.login()
                         
                    case '3':
                         Utils.limparTela()
                         self.ui.tituloDaFuncRich("Recuperar Senha", cor="green")
                         self.serv_user.recuperarSenha()
                         
                    case '0':
                         print("Até mais então...")
                         break
                    case _:
                         print("opção inválida") 
                         self.ui.pausar()
                         Utils.limparTela()                 


# Main:
if __name__ == "__main__":
     app = BemMais()
     app.menuInicial()