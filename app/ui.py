import time
from rich import box
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.text    import Text


class Ui:
     """Gerencia a camada de apresentação visual no terminal para o sistema BEM+.

     Esta classe centraliza toda a interação com o usuário que ocorre no
     terminal. Ela utiliza a biblioteca Rich para criar interfaces ricas e
     agradáveis, incluindo menus, painéis, tabelas e textos estilizados.

     """
    
     console = Console()
         
     def showMenu(self, titulo, itens, cor="yellow", limpar_tela: bool = True):
          """Exibe um menu estilizado e interativo no terminal.

          Utiliza a biblioteca Rich para criar uma tabela que serve como menu,
          com título, bordas e itens personalizáveis.

          Args:
               titulo (str): O cabeçalho a ser exibido no topo do menu.
               itens (list): Uma lista de tuplas, onde cada tupla contém
                    a chave da opção e sua descrição. Ex: [("1", "Login")].
               cor (str, optional): A cor principal para o título e borda do menu.
                    Padrão é "yellow".
               limpar_tela (bool, optional): Se True, limpa a tela antes de
                    exibir o menu. Padrão é True.
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
          """Orquestra e exibe a tela de menu inicial completa.

          Limpa a tela, mostra o banner principal, exibe uma mensagem de
          boas-vindas com efeito de digitação e, por fim, apresenta o menu
          com as opções iniciais (cadastro, login, etc.).

          Returns:
               str: A opção escolhida pelo usuário, sem espaços extras.
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
          """Exibe o menu principal do usuário logado.

          Apresenta um painel de boas-vindas com o nome do usuário e, em seguida,
          um menu com todas as funcionalidades principais do sistema BEM+.

          Args:
               nome (str): O nome do usuário logado para ser exibido no título.

          Returns:
               str: A opção de menu escolhida pelo usuário.
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
          """Exibe um título de seção padronizado e estilizado.

          Limpa a tela e mostra um painel que serve como cabeçalho para
          diferentes seções da aplicação, como "Cadastro" ou "Ranking".

          Args:
               titulo (str): O texto a ser exibido dentro do painel de título.
               cor (str, optional): A cor da borda e do texto do painel.
                    Padrão é "blue".
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


