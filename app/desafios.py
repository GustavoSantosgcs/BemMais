import json
import os
from .repo_usuario import RepoUsuario
from .utils import Utils


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

        Parâmetros:
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
        
        Parâmetros:
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
    def __init__(self, repo: RepoUsuario,
                 desafios_repo: ListaDesafios,
                 voucher_repo: RepoVoucher):
        """
        Inicializa o serviço de desafios com os repositórios necessários.

        Parâmetros:
            repo (RepoUsuario): Repositório de usuários.
            desafios_repo (ListaDesafios): Repositório de listas de desafios.
            voucher_repo (RepoVoucher): Repositório de vouchers.
        """
        self.users = repo
        self.desafios = desafios_repo
        self.vouchers = voucher_repo  
    
    
    # Menu interativo de desafios do bem
    def desafiosBem(self, email):
        """
        Exibe o menu de desafios e processa escolhas do usuário.

        Carrega o usuário, apresenta opções de desafios regulares, premium
        e histórico. Atualiza pontuação e persiste dados conforme fluxo.

        Parâmetros:
            email (str): Email do usuário logado.
        """
        user = self.users.buscar(email)
        codigos = self.vouchers.carregarCodigos()

        while True:
            Utils.limparTela()
            print("\n" + "="*32)
            print("🌟 MENU DESAFIOS 🌟".center(32))
            print("="*32)
            print("1 - Desafios regulares")
            print("2 - Desafios Premium")
            print("3 - Desafios realizados")
            print("0 - Voltar")
            print("="*32)
            escolha = input("Opção: ")

            match escolha:
                # Desafios normais
                case '1':
                    Utils.limparTela()
                    pendentes = [d for d in self.desafios.listarRegulares()
                                 if d not in user.desafios_realizados]
                    if not pendentes:
                        print("\nVocê já completou todos os desafios normais! 🎉")
                        continue

                    for i, d in enumerate(pendentes, 1):
                        print(f"[{i}] {d}")
                    print()
                    idx = input("Escolha o número do desafio (ou ENTER para voltar): ")
                    if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes)):
                        Utils.limparTela()
                        continue

                    selecao = pendentes[int(idx) - 1]
                    
                    print(f"\nVocê concluiu este desafio?\n{selecao}")
                    print("[1] Sim    [2] Não")
                    opcao = input("Opção: ").strip()
                    match opcao:
                        case '1':
                            user.pontos += 3
                            user.desafios_realizados.append(selecao)
                            print("Parabéns! Você ganhou 3 pontos pelo desafio!")
                            self.users.salvarUsuarios()
                        case '2':
                            print("Tudo bem, volte quando concluir! 👍")
                            input("Pressione Enter para continuar...")
                            Utils.limparTela()

                        case _:
                            print("Opção inválida!")
                            input("Pressione Enter para continuar...")
                            Utils.limparTela()

                # Desafios premium com interação do voucher
                case '2':  
                    Utils.limparTela()
                    pendentes_premium = [d for d in self.desafios.listarPremium()
                                         if d not in user.desafios_realizados]
                    if not pendentes_premium:
                        print("\nVocê já completou todos os desafios premium! Parabéns! 🎉")
                        continue
                    
                    print("Escolha o desafio premium:\n")
                    for i, d in enumerate(pendentes_premium):
                        print(f"{i+1}: {d}")
                    idx = input("(Digite o numero do desafio (ex:'1') ou pressione ENTER para voltar: ")
                    if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes_premium)):
                        continue

                    selecao = pendentes_premium[int(idx) - 1]
                    validos = codigos.get(selecao, [])
                    if not validos:
                        print("Nenhum voucher válido disponível para este premium.")
                        input("Pressione Enter para continuar...")
                        Utils.limparTela()
                        continue

                    print("\nPara validar este desafio premium, insira o voucher recebido:")
                    voucher = Utils.naoVazio("Voucher: ").strip()
                    if voucher in validos:
                        # Consome o voucher
                        validos.remove(voucher)
                        codigos[selecao] = validos
                        self.vouchers.salvarCodigos(codigos)

                        user.pontos += 10
                        user.desafios_realizados.append(selecao)
                        print("✅ Voucher aceito! Você ganhou 10 pontos! ✨")
                        self.users.salvarUsuarios()
                        input("Pressione Enter para continuar...")
                        Utils.limparTela()

                    else:
                        print("❌Voucher inválido ou já utilizado!")
                        input("Pressione Enter para continuar...")
                        Utils.limparTela()


                case '3':  
                    Utils.limparTela()
                    if not user.desafios_realizados:
                        print("\n🤔 Você ainda não completou nenhum desafio.")
                        input("Pressione Enter para continuar...")
                        Utils.limparTela()  
                    else:
                        print("\n✅ Desafios já concluídos:")
                        for d in user.desafios_realizados:
                            print(f" - {d}")
                        input("Pressione Enter para continuar...")
                        Utils.limparTela()       

                case '0':  
                    Utils.limparTela()
                    break

                case _:
                    print("Opção inválida, tente novamente.")
                    input("Pressione Enter para continuar...")
                    Utils.limparTela()