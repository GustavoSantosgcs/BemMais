def iniciar_dilema():
    pontuacao = 0
    print("\n Seja bem-vindo(a) ao DILEMAS ÉTICOS!")
    print("Responda as questões com as alternativas (a, b ou c):\n")

    perguntas = [
        {
            "pergunta": "Você encontra uma carteira com dinheiro no chão e ninguém por perto. O que faz?",
            "alternativas": {
                "a": "Leva até a polícia ou algum achado e perdido.",
                "b": "Fica com o dinheiro, mas tenta achar o dono.",
                "c": "Guarda tudo pra você."
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Você agiu como Kant: dever acima de tudo.",
                "b": "Você tentou equilibrar ética e resultado. Bem utilitarista.",
                "c": "Talvez não seja o caminho mais virtuoso..."
            }
        },
        {
            "pergunta": "Seu amigo está colando na prova. O professor não viu. E agora?",
            "alternativas": {
                "a": "Finge que nada viu.",
                "b": "Dá um toque discreto nele.",
                "c": "Entrega ele pro professor."
            },
            "resposta_certa": "b",
            "comentario": {
                "a": "Você escolheu se omitir. Às vezes é mais fácil, mas... é certo?",
                "b": "Você buscou o meio-termo e tentou educar. Aristóteles ficaria orgulhoso.",
                "c": "Você foi justo, mas talvez tenha perdido um amigo."
            }
        },
        {
            "pergunta": "Você pode mentir para proteger um amigo de um problema sério. O que faz?",
            "alternativas": {
                "a": "Mente pra protegê-lo.",
                "b": "Fala a verdade, mesmo que doa.",
                "c": "Tenta enrolar sem dizer nada diretamente."
            },
            "resposta_certa": "b",
            "comentario": {
                "a": "A intenção é boa, mas a mentira pode trazer consequências.",
                "b": "Você valoriza a verdade acima de tudo. Kant aprovaria.",
                "c": "Você tentou o caminho do meio. Pode funcionar, mas exige sabedoria."
            }
        }
    ]

    for i, pergunta in enumerate(perguntas, 1):
        print(f"\nPergunta {i}: {pergunta['pergunta']}")
        for letra, alternativa in pergunta["alternativas"].items():
            print(f"  ({letra}) {alternativa}")
        
        resposta = input("Sua resposta: ").lower()
        while resposta not in ['a', 'b', 'c']:
            resposta = input("Opção inválida. Escolha (a, b ou c): ").lower()

        if resposta == pergunta["resposta_certa"]:
            pontuacao += 1

        print(pergunta["comentario"][resposta])

    print(f"\n Você ganhou {pontuacao} ponto(s) nesse dilema!\n")
    return pontuacao
