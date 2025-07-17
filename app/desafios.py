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


VOUCHER = os.path.join('dados', 'codigos_premium.json')

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
        
    # Funções para carregar e salvar códigos de vouchers:
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

        Retorna:
            list[str]: Desafios regulares.
        """
        return list(self.regulares)
    
    def listarPremium(self):
        """
        Retorna uma cópia da lista de desafios premium.

        Retorna:
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
    
    # Menu interativo de desafios do bem
    def desafiosBem(self, email):
        """
        Exibe o menu interativo de desafios do bem.

        Apresenta ao usuário as opções:
        - Desafios Regulares: exibidos em lista com seleção e confirmação.
        - Desafios Premium: requerem validação via voucher.
        - Desafios Realizados: mostra histórico de desafios já cumpridos.

        Atualiza a pontuação e armazena os dados conforme necessário.

        Args:
            email (str): Email do usuário logado.
        """
        user = self.users.buscar(email)
        codigos = self.vouchers.carregarCodigos()

        while True:
            Utils.limparTela()
            self.ui.tituloDaFuncRich(titulo="🌟MENU DESAFIOS 🌟", cor="cyan")
            
            itens = [
                ("1", "Desafios Regulares"),
                ("2", "Desafios Premium"),
                ("3", "Desafios Realizados"),
                ("0", "Voltar")
            ]
            self.ui.showMenu("🌟 Desafios do Bem 🌟", itens, cor="green")
            escolha = self.ui.console.input("\n[bold]Escolha uma opção:[/bold] ").strip()

            match escolha:
                # Desafios regulares
                case '1':
                    Utils.limparTela()
                    pendentes = [d for d in self.desafios.listarRegulares()
                                 if d not in user.desafios_realizados]
                    if not pendentes:
                        self.ui.console.print("[yellow]Você já completou todos os desafios regulares![\yellow] 🎉")
                        self.ui.pausar()
                        continue
                    
                    # Tabela dos Regulares
                    tbl = Table(title="Desafios Regulares", box=box.ROUNDED, border_style="green", show_header=False, padding=(0,1))
                    tbl.add_column("#", style="cyan", justify="center")
                    tbl.add_column("Desafio", style="white")
                    for i, d in enumerate(pendentes, 1):
                        tbl.add_row(str(i), d)
                    self.ui.console.print(tbl)

                    # escolha do Desafio e verificação do input
                    idx = self.ui.console.input("\n[bold]Digite o número do desafio (ou ENTER para voltar):[/bold] ")
                    if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes)):
                        Utils.limparTela()
                        continue
                    selecao = pendentes[int(idx) - 1]
                    
                    # Painel de confirmação
                    painel = Panel(
                        Text(f"Você concluiu este desafio?\n\n{selecao}", justify="left"),
                        title="Confirmar Desafio",
                        border_style="green",
                        expand=False
                    )
                    self.ui.console.print(painel)
                    opcao = self.ui.console.input("[bold]1) Sim   2) Não[/bold] ").strip()
                    match opcao:
                        case '1':
                            user.pontos += 3
                            user.desafios_realizados.append(selecao)
                            print("Parabéns! Você ganhou 3 pontos pelo desafio!")
                            self.ui.pausar()
                            self.users.salvarUsuarios()
                        case '2':
                            print("Tudo bem, volte quando concluir! 👍")
                            self.ui.pausar()
                            Utils.limparTela()

                        case _:
                            print("Opção inválida!")
                            self.ui.pausar()
                            Utils.limparTela()

                # Desafios premium com interação do voucher
                case '2':  
                    Utils.limparTela()
                    pendentes_premium = [d for d in self.desafios.listarPremium()
                                         if d not in user.desafios_realizados]
                    if not pendentes_premium:
                        self.ui.console.print("[yellow]Você já completou todos os desafios Premium![\yellow] 🎉")
                        self.ui.pausar()
                        continue
                    
                    # Tabela Premium
                    tbl = Table(title="Desafios Premium", box=box.ROUNDED, border_style="green", show_header=False, padding=(0,1))
                    tbl.add_column("#", style="cyan", justify="center")
                    tbl.add_column("Desafio", style="white")
                    for i, d in enumerate(pendentes_premium, 1):
                        tbl.add_row(str(i), d)
                    self.ui.console.print(tbl)

                    # escolha do Desafio e verificação do input
                    idx = self.ui.console.input("\n[bold]Digite o número do desafio (ou ENTER para voltar):[/bold] ")
                    if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes_premium)):
                        continue

                    selecao = pendentes_premium[int(idx) - 1]
                    validos = codigos.get(selecao, [])
                    if not validos:
                        print("Nenhum voucher válido disponível para este premium.")
                        self.ui.pausar()
                        Utils.limparTela()
                        continue

                    print("\nPara validar este desafio premium, insira o voucher recebido:")
                    voucher = Utils.naoVazio("Voucher: ").strip()
                    with self.ui.console.status("[yellow]Verificando voucher...[/yellow]", spinner="dots"):
                        time.sleep(1)
                    if voucher in validos:
                        # Consome o voucher
                        validos.remove(voucher)
                        codigos[selecao] = validos
                        self.vouchers.salvarCodigos(codigos)

                        user.pontos += 30
                        user.desafios_realizados.append(selecao)
                        print("✅ Voucher aceito! Você ganhou 30 pontos! ✨")
                        self.users.salvarUsuarios()
                        self.ui.pausar()
                        Utils.limparTela()

                    else:
                        print("❌Voucher inválido ou já utilizado!")
                        self.ui.pausar()
                        Utils.limparTela()


                case '3':  
                    Utils.limparTela()
                    if not user.desafios_realizados:
                        self.ui.console.print("[yellow]🤔 Você ainda não completou nenhum desafio.[/yellow]")
                    else:
                        tbl = Table(title="Desafios Concluídos", box=box.ROUNDED, border_style="green")
                        tbl.add_column("#", style="cyan", width=3, justify="center")
                        tbl.add_column("Desafio", style="white")
                        for i, d in enumerate(user.desafios_realizados, 1):
                            tbl.add_row(str(i), d)
                        self.ui.console.print(tbl)
                    
                    self.ui.pausar()
                    Utils.limparTela()       

                case '0':  
                    Utils.limparTela()
                    break

                case _:
                    print("Opção inválida, tente novamente.")
                    self.ui.pausar()
                    Utils.limparTela()