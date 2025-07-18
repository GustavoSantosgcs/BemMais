import json
import os
import time
from .repo_usuario import RepoUsuario
from .utils import Utils
from .ui import Ui
from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Console 

VOUCHER = os.path.join('dados', 'codigos_premium.json')

# Projetos parceiros 
PARCEIROS = [
    {
        "nome": "ECODROP",
        "descricao": "A ideia do projeto é ser um sistema para condomínios que estimule as pessoas a gastar menos água no dia a dia. Caso o objetivo seja alcançado,"
        " o usuário ganhará pontos para trocar por recompensas.",
        "url": "https://github.com/Matheuscastro1903/projetova1.git"
    },
    {
        "nome": "P.A.T.A.S.",
        "descricao": "O P.A.T.A.S. nasceu para resolver um problema central enfrentado por ONGs e projetos voluntários de resgate animal:"
        " a falta de uma ferramenta centralizada e acessível para gerir o fluxo de animais. A plataforma oferece uma solução tecnológica"
        " robusta, construída em Python, que permite o controle total sobre o registo de animais, o acompanhamento do seu estado de saúde"
        " e a sua eventual disponibilização para uma adoção responsável. Com uma interface gráfica intuitiva, o objetivo é otimizar o trabalho dos voluntários"
        " e criar uma ponte transparente e de confiança com a comunidade de adotantes.",
        "url": "https://github.com/DhaviRodrigues/p_a_t_a_s_.git"
    },
    {
        "nome": "Pernambuco Cultural",
        "descricao": "Pernambuco cultural é um projeto que visa propiciar aos seus usuários maior exposição e contato com eventos regionais de Pernambuco por meio de"
        " um divulgador de eventos e também incentivar o acesso a obras literárias de caráter regional e universal por meio de um sistema baseado na gamificação, por meio de"
        " jogos e testes de conhecimento acerca de obras literárias, assim dinamizando o processo de aprendizado, através da leitura e propiciando uma maior exposição da riqueza cultural Pernambucana para o mundo.",
        "url": "https://github.com/LucaSs55/projeto1-pernambuco_cultural.git"
    },
    {
        "nome": "Central de achados e perdidos UFRPE",
        "descricao": "O projeto foi pensado com a ideia de solucionar um problema simples, que até hoje não foi feito nenhuma medida realmente efetiva. A partir da"
        " central de achados ufrpe, os estudantes e até mesmo funcionários, terão a oportunidade de ter acesso à uma plataforma em que poderão compartilhar objetos "
        "que a pessoa perdeu, ou que ela deseja encontrar. Facilitando assim, o alcance e a segurança na devolução do objeto a seu dono.",
        "url": "https://github.com/leolafa/central-de-achados-ufrpe.git"
    }
]

class RepoVoucher:
    """
    Repositório para carregar e salvar vouchers de desafios premium em JSON.

    A classe gerencia o arquivo de vouchers, fornecendo métodos para leitura e gravação
    de um mapeamento de texto de desafio para listas de códigos válidos.
    """
    
    def __init__(self, caminho = VOUCHER):
        """
        Repositório para carregar e salvar vouchers de desafios premium.

        Args:
            caminho (str): Caminho para o arquivo JSON de vouchers.
        """
        self.caminho = caminho
        
    def carregarCodigos(self):
        """
        Lê e retorna o dicionário de vouchers do arquivo JSON ou retorna
        um dicionário vazio caso o arquivo não exista.
        """
        if os.path.exists(self.caminho):
            with open(self.caminho, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        return {}

    def salvarCodigos(self, cods):
        """
        Salva arquivo de códigos, de maneira estruturada, em formato JSON.
        
        Args:
            cods (dict[str, list[str]]): Mapeamento de desafio -> lista de códigos a salvar.
        """         
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(cods, arquivo, indent=2, ensure_ascii=False)


class ListaDesafios:
    """
    Provê listas de desafios regulares e premium do BEM+.

    Armazena as listas internamente e disponibiliza métodos para acesso seguro.
    """
    def __init__(self):
        """
        Inicializa as listas de desafios regulares e premium.
        """
            
        # Listas de desafios regulares:
        self.regulares = [
            "💬 Inicie uma conversa com alguém novo hoje e deseje um bom dia sincero.",
            "🧺 Separe roupas ou alimentos que não usa mais e doe para quem precisa.",
            "🌟 Faça um elogio genuíno a alguém que esteja precisando de motivação.",
            "📵 Fique 1 hora longe do celular e aproveite para dar atenção total a alguém.",
            "🤝 Ajude uma pessoa idosa com sacolas ou atravessar a rua com segurança.",
            "📝 Escreva uma mensagem positiva (bilhete, WhatsApp ou e-mail) para alguém importante na sua vida.",
            "😊 Ofereça ajuda a um colega que esteja com dificuldades, mesmo que ele não peça.",
            "💖 Envie uma mensagem agradecendo alguém que te inspirou ou te ajudou recentemente.",
            "🌱 Plante algo (pode ser uma muda ou até um grão) e cuide por uma semana.",
            "📚 Doe um livro que você já leu para alguém que possa gostar dele."
        ]

        # Listas de desafios Premium:
        self.premium = [
            "🎭 Levar alguém a um evento cultural (colaboração Pernamb. Cultural).",
            "🚿 Reduzir o consumo de água em casa por uma semana (EcoDrop).",
            "🐾 Realizar adoção de um animal (Projeto P.A.T.A.S.)",
            "🐾 Visitar os animais abrigados (Projeto P.A.T.A.S.)",
            "🔍 Encontrar e devolver item perdido (Central de Achados e Perdidos UFRPE)"
        ]

    def listarRegulares(self):
        """
        Retorna uma cópia da lista de desafios regulares.

        Returns:
            list[str]: Desafios regulares.
        """
        return list(self.regulares)
    
    def listarPremium(self):
        """
        Retorna uma cópia da lista de desafios premium.

        Returns:
            list[str]: Desafios premium.
        """
        return list(self.premium)


class DesafioBem:
    """
    Serviço interativo de desafios do BEM+.

    Orquestra a exibição e conclusão de desafios regulares e premium,
    atualizando pontos do usuário e consumindo vouchers conforme necessário.
    """
    
    def __init__(self, repo: RepoUsuario, desafios_repo: ListaDesafios,
                 voucher_repo: RepoVoucher, ui: Ui):
        """
        Inicializa o serviço de desafios com os repositórios e a interface de usuário.

        Args:
            repo (RepoUsuario): Repositório de usuários.
            desafios_repo (ListaDesafios): Repositório de listas de desafios.
            voucher_repo (RepoVoucher): Repositório de vouchers.
            ui (Ui): Camada de apresentação para interação com o usuário.
        """
        self.users = repo
        self.desafios = desafios_repo
        self.vouchers = voucher_repo  
        self.ui = ui
        self.console = Console() 

    def apresentarParceiros(self):
        """
        Exibe as informações dos projetos parceiros de forma formatada.
        """
        Utils.limparTela()
        self.ui.tituloDaFuncRich("🤝 Projetos Parceiros 🤝", "yellow")
        
        for parceiro in PARCEIROS:
            info_parceiro = Text()
            info_parceiro.append(parceiro["descricao"], style="white")
            info_parceiro.append("\n\n🔗 GitHub: ", style="bold cyan")
            info_parceiro.append(parceiro["url"], style="underline cyan")

            painel_parceiro = Panel(
                info_parceiro,
                title=f"[bold green]{parceiro['nome']}[/bold green]",
                border_style="green",
                expand=False,
                padding=(1, 2)
            )
            self.console.print(painel_parceiro)
        
        self.ui.pausar()

    def processarDesafiosPremium(self, user, codigos):
        """
        Lida com a lógica de listar, selecionar e validar desafios premium.
        
        Args:
            user (Usuario): O objeto do usuário logado.
            codigos (dict): O dicionário de códigos de voucher carregado.
        """
        Utils.limparTela()
        pendentes_premium = [d for d in self.desafios.listarPremium()
                             if d not in user.desafios_realizados]
        if not pendentes_premium:
            self.console.print("\n[bold yellow]Você já completou todos os desafios Premium![/bold yellow] 🎉\n")
            self.ui.pausar()
            return

        # Tabela Premium
        tbl = Table(title="Desafios Premium Disponíveis", box=box.ROUNDED, border_style="gold1", show_header=False, padding=(0, 1))
        tbl.add_column("#", style="cyan", justify="center")
        tbl.add_column("Desafio", style="white")
        for i, d in enumerate(pendentes_premium, 1):
            tbl.add_row(str(i), d)
        self.console.print(tbl)

        # Escolha do Desafio
        idx = self.console.input("\n[bold]Digite o número do desafio (ou ENTER para voltar):[/bold] ")
        if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes_premium)):
            return

        selecao = pendentes_premium[int(idx) - 1]
        validos = codigos.get(selecao, [])
        if not validos:
            self.console.print("\n[bold red]Nenhum voucher válido disponível para este desafio.[/bold red]")
            self.ui.pausar()
            return

        self.console.print("\n[bold]Para validar este desafio premium, insira o voucher recebido:[/bold]")
        voucher = Utils.naoVazio("Voucher: ").strip()
        with self.console.status("[yellow]Verificando voucher...[/yellow]", spinner="dots"):
            time.sleep(1)
            
        if voucher in validos:
            # Consome o voucher
            validos.remove(voucher)
            codigos[selecao] = validos
            self.vouchers.salvarCodigos(codigos)

            user.pontos += 30
            user.desafios_realizados.append(selecao)
            self.users.salvarUsuarios()
            self.console.print("\n[bold green]✅ Voucher aceito! Você ganhou 30 pontos! ✨[/bold green]")
        else:
            self.console.print("\n[bold red]❌ Voucher inválido ou já utilizado![/bold red]")
        
        self.ui.pausar()

# Menu principal do Desafios do Bem
    def desafiosBem(self, email):
        """
        Exibe o menu interativo de desafios do bem.
        """
        user = self.users.buscar(email)
        codigos = self.vouchers.carregarCodigos()

        while True:
            Utils.limparTela()
            self.ui.tituloDaFuncRich("🌟 MENU DESAFIOS 🌟", "cyan")
            
            itens_principais = [
                ("1", "Desafios Regulares"),
                ("2", "Desafios Premium"),
                ("3", "Desafios Realizados"),
                ("0", "Voltar")
            ]
            self.ui.showMenu("🌟 Desafios do Bem 🌟", itens_principais, cor="green")
            escolha = self.ui.console.input("\n[bold]Escolha uma opção:[/bold] ").strip()
            match escolha:
                case '1': # Desafios Regulares
                    Utils.limparTela()
                    pendentes = [d for d in self.desafios.listarRegulares()
                                if d not in user.desafios_realizados]
                    if not pendentes:
                        self.console.print("\n[yellow]Você já completou todos os desafios regulares![/yellow] 🎉\n")
                        self.ui.pausar()
                        continue
                    
                    tbl = Table(title="Desafios Regulares", box=box.ROUNDED, border_style="green", show_header=False, padding=(0,1))
                    tbl.add_column("#", style="cyan", justify="center")
                    tbl.add_column("Desafio", style="white")
                    for i, d in enumerate(pendentes, 1):
                        tbl.add_row(str(i), d)
                    self.console.print(tbl)

                    idx = self.console.input("\n[bold]Digite o número do desafio (ou ENTER para voltar):[/bold] ")
                    if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes)):
                        continue
                    
                    selecao = pendentes[int(idx) - 1]
                    
                    painel = Panel(
                        Text(f"Você concluiu este desafio?\n\n{selecao}", justify="left"),
                        title="Confirmar Desafio", border_style="green", expand=False
                    )
                    self.console.print(painel)
                    opcao = self.console.input("[bold]1) Sim   2) Não[/bold] ").strip()
                    
                    match opcao:
                        case "1":
                            user.pontos += 3
                            user.desafios_realizados.append(selecao)
                            self.users.salvarUsuarios()
                            self.console.print("\n[bold green]Parabéns! Você ganhou 3 pontos pelo desafio![/bold green]")
                        case "2":
                            self.console.print("\n[bold yellow]Tudo bem, volte quando concluir! 👍[/bold yellow]")
                        case _:
                            self.console.print("\n[bold red]Opção inválida![/bold red]")
                    self.ui.pausar()

                case "2": # Desafios Premium 
                    while True:
                        Utils.limparTela()
                        self.ui.tituloDaFuncRich("💎 DESAFIOS PREMIUM 💎", "gold1")
                        itens_premium = [
                            ("1", "Conhecer Projetos Parceiros"),
                            ("2", "Listar Desafios Premium"),
                            ("0", "Voltar")
                        ]
                        self.ui.showMenu("🌟 Menu Premium 🌟", itens_premium, cor="yellow")
                        opcao_premium = self.console.input("\n[bold]Escolha uma opção:[/bold] ").strip()

                        if opcao_premium == '1':
                            self.apresentarParceiros()
                        elif opcao_premium == '2':
                            self.processarDesafiosPremium(user, codigos)
                        elif opcao_premium == '0':
                            break
                        else:
                            self.console.print("\n[bold red]Opção inválida, tente novamente.[/bold red]")
                            self.ui.pausar()

                case "3": # Desafios Realizados
                    Utils.limparTela()
                    if not user.desafios_realizados:
                        self.console.print("\n[yellow]🤔 Você ainda não completou nenhum desafio.[/yellow]\n")
                    else:
                        tbl = Table(title="Desafios Concluídos", box=box.ROUNDED, border_style="green")
                        tbl.add_column("#", style="cyan", width=3, justify="center")
                        tbl.add_column("Desafio", style="white")
                        for i, d in enumerate(user.desafios_realizados, 1):
                            tbl.add_row(str(i), d)
                        self.console.print(tbl)
                    self.ui.pausar()

                case "0":
                    Utils.limparTela()
                    break

                case _:
                    self.console.print("\n[bold red]Opção inválida, tente novamente.[/bold red]")
                    self.ui.pausar()