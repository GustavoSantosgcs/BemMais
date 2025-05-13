def iniciar_dilema():
    pontuacao = 0
    print("\n Seja bem-vindo(a) ao CENÁRIOS ÉTICOS!")
    print("Responda as questões com as alternativas (a, b ou c):\n")

#Perguntas:
    perguntas = [
        {
            "pergunta": "Você descobre uma falha de segurança grave no sistema da empresa onde trabalha. O que faz?",
            "alternativas": {
                "a": "Comunica imediatamente ao chefe ou à equipe de segurança.",
                "b": "Usa a falha para ganhar alguma vantagem discreta.",
                "c": "Ignora, afinal, não é problema seu."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Responsabilidade profissional! Você age de forma ética e protege a empresa.",
                "b": "Ética duvidosa! Você priorizou interesses pessoais sobre a segurança.",
                "c": "Indiferença pode gerar grandes danos. A omissão também é antiética."
            }
        },
        {
            "pergunta": "Você é contratado para desenvolver um sistema, mas o cliente pede que você copie partes de um software de outra empresa sem autorização. O que você faz?",
            "alternativas": {
                "a": "Recusa a tarefa e explica as implicações legais e éticas.",
                "b": "Copia disfarçadamente, tentando não deixar rastros.",
                "c": "Faz o que o cliente pede; afinal, ele está pagando."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Excelente! Você respeitou os direitos autorais e a ética profissional.",
                "b": "Risco altíssimo! Pode gerar processos e prejudicar sua carreira.",
                "c": "Errado! O pagamento não justifica quebrar a lei e a ética."
            }
        },
        {
            "pergunta": "Durante um projeto, você percebe que um colega está plagiando códigos de fontes públicas sem dar os devidos créditos. Você:",
            "alternativas": {
                "a": "Conversa com ele e explica as implicações.",
                "b": "Informa a liderança ou professor responsável.",
                "c": "Ignora, pois não é problema seu."
            },
            "pontuações": {
                "a": 0,
                "b": 5,
                "c": 0
            },
            "resposta_certa": "b",
            "comentario": {
                "a": "Boa tentativa, mas talvez precise envolver alguém com mais autoridade.",
                "b": "Correto! Você toma uma ação ética e responsável.",
                "c": "A omissão pode ter consequências graves para todos."
            }
        },
        {
            "pergunta": "Você pode mentir para proteger um amigo de um problema sério. O que faz?",
            "alternativas": {
                "a": "Mente pra protegê-lo.",
                "b": "Fala a verdade, mesmo que doa.",
                "c": "Tenta enrolar sem dizer nada diretamente."
            },
            "pontuações": {
                "a": 0,
                "b": 5,
                "c": 0
            },
            "resposta_certa": "b",
            "comentario": {
                "a": "A intenção é boa, mas a mentira pode trazer consequências.",
                "b": "Você valoriza a verdade acima de tudo. Kant aprovaria.",
                "c": "Você tentou o caminho do meio. Pode funcionar, mas exige sabedoria."
            }
        },
        {
            "pergunta": "Você tem acesso a dados pessoais de usuários na empresa. Um amigo pede para você passar algumas informações. O que você faz?",
            "alternativas": {
                "a": "Recusa e explica que isso é confidencial.",
                "b": "Passa só algumas informações menos importantes.",
                "c": "Entrega os dados completos, afinal é só um amigo."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Excelente postura ética! Confidencialidade é essencial em TI.",
                "b": "Ainda é uma quebra de confiança e pode ter consequências.",
                "c": "Gravíssimo! Você quebrou a privacidade e a confiança do usuário."
            }
        },
        {
            "pergunta": "Você encontra um script online que promete burlar o licenciamento de um software caro que sua equipe precisa. Você:",
            "alternativas": {
                "a": "Nem pensa nisso e busca alternativas legais.",
                "b": "Testa o script só por curiosidade.",
                "c": "Usa o script para economizar no projeto."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Postura correta! Pirataria nunca é solução.",
                "b": "Curiosidade pode custar caro — evite tentações antiéticas.",
                "c": "Errado! Economizar quebrando a lei não é justificável."
            }
        },
        {
            "pergunta": "Seu chefe pede para acelerar o projeto, mesmo que precise 'dar um jeitinho' nos testes de segurança. Você:",
            "alternativas": {
                "a": "Explica os riscos e se recusa a pular etapas.",
                "b": "Dá um jeito rápido, prometendo revisar depois.",
                "c": "Pula os testes e entrega logo para agradar."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Corretíssimo! Qualidade e segurança vêm antes de pressa.",
                "b": "Perigoso! Depois pode ser tarde demais para corrigir.",
                "c": "Uma decisão antiética que pode gerar prejuízo enorme."
            }
        },
        {
            "pergunta": "Você está saindo de uma empresa e pensa em copiar o código que desenvolveu lá para usar em projetos futuros. Você:",
            "alternativas": {
                "a": "Sai apenas com seu conhecimento e deixa o código para a empresa.",
                "b": "Copia partes pequenas achando que não fará falta.",
                "c": "Copia tudo, afinal foi você quem escreveu."
            },
            "pontuações": {
                "a": 5,
                "b": 0,
                "c": 0
            },
            "resposta_certa": "a",
            "comentario": {
                "a": "Parabéns! Ética até o último dia de trabalho.",
                "b": "Ainda é errado; propriedade intelectual não é sua.",
                "c": "Não importa quem escreveu — o código pertence à empresa."
            }
        }
    ]


#Funções:
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\nPergunta {i}: {pergunta['pergunta']}")
        for letra, alternativa in pergunta["alternativas"].items():
            print(f"  ({letra}) {alternativa}")
        
        resposta = input("Sua resposta: ").lower()
        while resposta not in ['a', 'b', 'c']:
            resposta = input("Opção inválida. Escolha (a, b ou c): ").lower()

        pontos_resposta = pergunta.get("pontuações", {}).get(resposta, 0)
        pontuacao += pontos_resposta
        
        print(f"✅ Você ganhou {pontos_resposta} ponto(s) nesta pergunta.")
        print(pergunta["comentario"][resposta])

    print(f"\n Você ganhou {pontuacao} ponto(s) nesse dilema!\n")
    return pontuacao
