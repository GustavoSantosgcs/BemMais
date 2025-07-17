import time
from rich import box
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.text    import Text


class Ui:
     """
    Camada de apresentação do sistema BEM+.

    Responsável por toda interação visual no terminal, incluindo:
    - Impressão de menus estilizados com Rich;
    - Exibição de banners e títulos;
    - Escrita com efeito de máquina de escrever;
    - Pausas e prompts ao usuário.
    """
    
     console = Console()
         
     def showMenu(self, titulo, itens, cor="yellow", limpar_tela: bool = True):
          """
          Exibe um menu rico no terminal usando Rich:
          - titulo: cabeçalho 
          - itens: lista de tuplas (chave, descrição)
          - cor: cor principal
          - limpar_tela: True para console.clear(), False para não limpar
          """
          
          if limpar_tela:
               self.console.clear()
          
          table = Table(
               title=f"[bold {cor}]{titulo}[/bold {cor}]",
               box=box.ROUNDED,
               border_style=cor,
               padding=(0,1),
               show_header=False
          )
          table.add_column("Opção", style="cyan", justify="center")
          table.add_column("Descrição", style="white")
          for key, desc in itens:
               table.add_row(key, desc)
          self.console.print(table)
     
     def menuInicialRich(self):
          """
          Mostra o banner, faz a entrada dramática, aguarda,
          limpa e exibe o menu inicial. Retorna a opção escolhida.
          """

          self.console.clear()
          self.bannerPrincipal()
          self.escrever("Bem-vindo(a) ao BEM+!",delay=0.02)
          Ui.pausar()
          
          # Funções do menu
          itens = [
               ("1", "Cadastrar usuário"),
               ("2", "Login"),
               ("3", "Recuperar senha"),
               ("0", "Sair"),
          ]
          # Exibe o menu
          self.showMenu("Menu Inicial", itens, cor="magenta")

          opcao = self.console.input("\n[bold]Escolha uma opção:[/bold] ")
          return opcao.strip()
     
     def menuBemRich(self, nome):
          """
          Exibe o menu principal do BEM+ estilizado e retorna a opção escolhida.
          """
          
          self.console.clear()
          titulo = Text(f"🌟 MENU BEM+ – {nome} 🌟", style="bold green")
          self.console.print(Panel(titulo, expand=True, border_style="green"))
          
          # Funcionalidades do menu
          itens = [
               ("1", "Frase do Dia"),
               ("2", "Iniciar Cenário Ético"),
               ("3", "Desafios do Bem"),
               ("4", "Ver Pontuação e Nível"),
               ("5", "Ranking de Usuários"),
               ("6", "Histórico de Respostas"),
               ("0", "Sair do menu BEM+")
          ]
          
          self.showMenu(titulo, itens, cor="green")
          
          return self.console.input("\n[bold]Sua opção é?[/bold] ").strip()
          
     def tituloDaFuncRich(self, titulo, cor="blue"):
          """
          Limpa a tela e exibe um cabeçalho padronizado para uma seção.
          - titulo: nome da funcionalidade (ex: "Cadastro de Usuário")
          - cor: cor principal do painel
          """
          self.console.clear()
          header = Text(f"🔹 {titulo} 🔹", style=f"bold {cor}")
          self.console.print(Panel(header, expand=False, border_style=cor))
             
     @staticmethod
     def pausar():
          """
          Pausa a execução até o usuário pressionar Enter.
          """
          Ui.console.input("\n[grey]Pressione Enter para continuar...[/grey]")

     def escrever(self, texto, delay=0.02,style=None):
          """
          Imprime o texto caractere por caractere, simulando uma máquina de escrever.

          Args:
               texto (str): Texto a ser exibido.
               delay (float): Intervalo entre cada caractere.
               style (str, optional): Estilo Rich a ser aplicado.
          """
          for c in texto:
               if style:
                    self.console.print(c, end="", style=style, highlight=False)
               
               else:
                    print(c, end='', flush=True)
               time.sleep(delay)
          print()
          
     def bannerPrincipal(self):
          """Exibe o ASCII-art do banner."""
          
          title = (
               "\n"
               " ██████╗  ███████╗ ███╗   ███╗          \n"
               " ██╔══██╗ ██╔════╝ ████╗ ████║   ╔██╗   \n"
               " ██████╔╝ █████╗   ██╔████╔██║  ██████  \n"
               " ██╔══██╗ ██╔══╝   ██║╚██╔╝██║   ╚██╝   \n"
               " ██████╔╝ ███████╗ ██║ ╚═╝ ██║          \n"
               " ╚═════╝  ╚══════╝ ╚═╝     ╚═╝          \n"
          )
          self.console.print(f"[cyan bold]{title}[/cyan bold]", justify="left")


