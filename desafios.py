import random

def desafios_bem(usuarios, email):
    desafios = [
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

    desafio_semana = random.choice(desafios)
    print(f"\n🌟 Desafio da Semana 🌟\n{desafio_semana}\n")

    while True:
        print("Você já realizou este desafio?")
        print("[1] Sim")
        print("[2] Não")
        print("[3] Voltar")
        opcao = input("Opção: ")

        if opcao == '1':
            usuarios[email]['pontos'] += 10  
            print("Parabéns! Você ganhou 10 pontos pelo desafio!")
            break
        elif opcao == '2':
            print("Tudo bem! Quem sabe na próxima.")
            break
        elif opcao == '3':
            print("Voltando ao menu...")
            break
        else:
            print("Opção inválida, tente novamente.")
