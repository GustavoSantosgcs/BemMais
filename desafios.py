import json
import os
from utils import nao_vazio, limpar_tela

COD_PREMIUM = os.path.join('dados', 'codigos_premium.json')


# Funções para carregar e salvar códigos de vouchers:
def carregar_codigos():
    if os.path.exists(COD_PREMIUM):
        with open(COD_PREMIUM, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return {}


def salvar_codigos(cods):
    os.makedirs(os.path.dirname(COD_PREMIUM), exist_ok=True)
    with open(COD_PREMIUM, 'w', encoding='utf-8') as arquivo:
        json.dump(cods, arquivo, indent=2, ensure_ascii=False)


# Listas de desafios normais
desafios_regulares = [
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


# Listas de desafios normais
desafios_premium = [
    "🎭 Levar alguém a um evento cultural (colaboração Pernamb. Cultural).",
    "🚿 Reduzir o consumo de água em casa por uma semana (EcoDrop).",
    "🐾 Realizar adoção de um animal (Projeto P.A.T.A.S.)",
    "🐾 Visitar os animais abrigados (Projeto P.A.T.A.S.)",
    "🔍 Encontrar e devolver item perdido (Central de Achados e Perdidos UFRPE)"
]


# Menu interativo de desafios do bem
def desafios_bem(repo, email):
    """
    Exibe e gerencia o menu de desafios (regulares e premium), atualizando pontos
    e histórico de desafios realizados.

    Parâmetros:
        repo (RepoUsuario): repositório de usuários persistido em JSON.
        email (str): email do usuário atualmente logado.
    """
    user = repo.buscar(email)
    codigos = carregar_codigos()

    while True:
        limpar_tela()
        print("\n" + "="*32)
        print("🌟 MENU DESAFIOS 🌟".center(32))
        print("="*32)
        print("1 - Desafios a serem realizados")
        print("2 - Desafios Premium")
        print("3 - Desafios realizados")
        print("0 - Voltar")
        print("="*32)
        escolha = input("Opção: ")

        match escolha:
            # Desafios normais
            case '1':
                limpar_tela()
                pendentes = [d for d in desafios_regulares if d not in user.desafios_realizados]
                if not pendentes:
                    print("\nVocê já completou todos os desafios normais! 🎉")
                    continue

                for i, d in enumerate(pendentes, 1):
                    print(f"[{i}] {d}")
                idx = input("Escolha o número do desafio (ou ENTER para voltar): ")
                if not idx.isdigit() or not (1 <= int(idx) <= len(pendentes)):
                    limpar_tela()
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
                        repo.salvar_usuarios()
                    case '2':
                        print("Tudo bem, volte quando concluir! 👍")
                        input("Pressione Enter para continuar...")
                        limpar_tela()

                    case _:
                        print("Opção inválida!")
                        input("Pressione Enter para continuar...")
                        limpar_tela()

            # Desafios premium com interação do voucher
            case '2':  
                limpar_tela()
                pendentes_premium = [d for d in desafios_premium if d not in user.desafios_realizados]
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
                    limpar_tela()
                    continue

                print("\nPara validar este desafio premium, insira o voucher recebido:")
                voucher = nao_vazio("Voucher: ").strip()
                if voucher in validos:
                    # Consome o voucher
                    validos.remove(voucher)
                    codigos[selecao] = validos
                    salvar_codigos(codigos)

                    user.pontos += 10
                    user.desafios_realizados.append(selecao)
                    print("✅ Voucher aceito! Você ganhou 10 pontos! ✨")
                    repo.salvar_usuarios()
                    input("Pressione Enter para continuar...")
                    limpar_tela()

                else:
                    print("❌Voucher inválido ou já utilizado!")
                    input("Pressione Enter para continuar...")
                    limpar_tela()


            case '3':  
                limpar_tela()
                if not user.desafios_realizados:
                    print("\nVocê ainda não completou nenhum desafio.")
                else:
                    print("\n✅ Desafios já concluídos:")
                    for d in user.desafios_realizados:
                        print(f" - {d}")
                    input("Pressione Enter para continuar...")
                    limpar_tela()       

            case '0':  
                limpar_tela()
                break

            case _:
                print("Opção inválida, tente novamente.")



