import random
import time
from usuario import salvar_usuarios


#Lista de perguntas com as alternativas e comentários
PERGUNTAS = [
    {
        "pergunta": "💧 No projeto EcoDrop, você percebe que os dados de consumo de água estão\n"
        "sendo ajustados manualmente para aparentar melhor desempenho. O que você faz?",
        "alternativas": {
            "a": "Reporta o erro à equipe e solicita correção imediata.",
            "b": "Ignora, afinal a meta foi cumprida no fim das contas.",
            "c": "Continua usando os dados alterados e não documenta nada."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "👏 Ótimo! Transparência e precisão são fundamentais em projetos ambientais.",
            "b": "🤔 Metas importam, mas ética e qualidade dos dados vêm antes.",
            "c": "🚨 Ajustes não documentados comprometem toda a credibilidade do projeto."
        }
    },
    {
        "pergunta": "🐾 No projeto P.A.T.A.S., um adotante devolve o animal após\n"
        "poucos dias sem explicar o motivo. Você: ",
        "alternativas": {
            "a": "Aceita a devolução sem questionar, pois não é sua responsabilidade.",
            "b": "Tenta entender os motivos e oferece suporte para novo acolhimento.",
            "c": "Critica o adotante publicamente para evitar que outros repitam o erro."
        },
        "pontuações": {"a": 0, "b": 1, "c": 0},
        "resposta_certa": "b",
        "comentario": {
            "a": "☹️ Ética exige preocupação pelo bem‐estar do animal,\n"
            "não só comodidade do adotante.",
            "b": "👍 Empatia e ação proativa ajudam a melhorar todo o processo de adoção.",
            "c": "⚠️ Expor alguém pode gerar constrangimento e não resolve o problema."
        }
    },
    {
        "pergunta": "🐾 Através do projeto P.A.T.A.S., você agendou uma visita e, ao chegar ao\n"
        "local, percebe que alguns animais estão estressados e em condições inadequadas. Você:",
        "alternativas": {
            "a": "Registra as condições e informa imediatamente a coordenação do abrigo.",
            "b": "Fica em silêncio para não atrapalhar a rotina do abrigo.",
            "c": "Compartilha fotos nas redes sociais sem falar com os responsáveis."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "✅ Responsabilidade e cuidado ajudam a melhorar as condições do abrigo.",
            "b": "❌ Silêncio pode prolongar problemas e prejudicar os animais.",
            "c": "❌ Expor antes de apurar pode causar pânico e prejudicar a instituição."
        }
    },
    {
        "pergunta": "🔍 Na Central de Achados e Perdidos UFRPE, você encontra um item de valor\n"
        "sem registro eletrônico do dono. O que faz?",
        "alternativas": {
            "a": "Guarda o item no arquivo físico e informa a todos os canais oficiais para devolução.",
            "b": "Fica com o item até alguém ‘aparecer’ pedindo.",
            "c": "Descarta o item para não ter dor de cabeça."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "✅ Exibir responsabilidade e seguir o procedimento garante confiança no serviço.",
            "b": "❌ Reter sem registro diminui a transparência e prejudica o usuário.",
            "c": "❌ Descartar algo de valor é negligência e fere o propósito do projeto."
        }
    },
    {
        "pergunta": "💻 Você descobre uma falha de segurança grave no sistema da empresa onde\n"
        "trabalha. O que faz?",
        "alternativas": {
            "a": "Comunica imediatamente ao chefe ou à equipe de segurança.",
            "b": "Usa a falha para ganhar alguma vantagem discreta.",
            "c": "Ignora, afinal, não é problema seu."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Responsabilidade profissional! Você age de forma ética e protege a empresa.",
            "b": "Ética duvidosa! Você priorizou interesses pessoais sobre a segurança.",
            "c": "Indiferença pode gerar grandes danos. A omissão também é antiética."
        }
    },
    {
        "pergunta": "🖥️ Você é contratado para desenvolver um sistema, mas o cliente pede que você\n"
        "copie partes de um software de outra empresa sem autorização. O que você faz?",
        "alternativas": {
            "a": "Recusa a tarefa e explica as implicações legais e éticas.",
            "b": "Copia disfarçadamente, tentando não deixar rastros.",
            "c": "Faz o que o cliente pede; afinal, ele está pagando."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Excelente! Você respeitou os direitos autorais e a ética profissional.",
            "b": "Risco altíssimo! Pode gerar processos e prejudicar sua carreira.",
            "c": "Errado! O pagamento não justifica quebrar a lei e a ética."
        }
    },
    {
        "pergunta": "📄 Durante um projeto, você percebe que um colega está plagiando códigos\n"
        "de fontes públicas sem dar os devidos créditos. Você:",
        "alternativas": {
            "a": "Conversa com ele e explica as implicações.",
            "b": "Informa a liderança ou professor responsável.",
            "c": "Ignora, pois não é problema seu."
        },
        "pontuações": {"a": 0, "b": 1, "c": 0},
        "resposta_certa": "b",
        "comentario": {
            "a": "Boa tentativa, mas talvez precise envolver alguém com mais autoridade.",
            "b": "Correto! Você toma uma ação ética e responsável.",
            "c": "A omissão pode ter consequências graves para todos."
        }
    },
    {
        "pergunta": "🤥 Você pode mentir para proteger um amigo de um problema sério. O que faz?",
        "alternativas": {
            "a": "Mente pra protegê-lo.",
            "b": "Fala a verdade, mesmo que doa.",
            "c": "Tenta enrolar sem dizer nada diretamente."
        },
        "pontuações": {"a": 0, "b": 1, "c": 0},
        "resposta_certa": "b",
        "comentario": {
            "a": "A intenção é boa, mas a mentira pode trazer consequências.",
            "b": "Você valoriza a verdade acima de tudo. Kant aprovaria.",
            "c": "Você tentou o caminho do meio. Pode funcionar, mas exige sabedoria."
        }
    },
    {
        "pergunta": "🔒 Você tem acesso a dados pessoais de usuários na empresa.\n"
        "Um amigo pede para você passar algumas informações. O que você faz?",
        "alternativas": {
            "a": "Recusa e explica que isso é confidencial.",
            "b": "Passa só algumas informações menos importantes.",
            "c": "Entrega os dados completos, afinal é só um amigo."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Excelente postura ética! Confidencialidade é essencial em TI.",
            "b": "Ainda é uma quebra de confiança e pode ter consequências.",
            "c": "Gravíssimo! Você quebrou a privacidade e a confiança do usuário."
        }
    },
    {
        "pergunta": "💻 Você encontra um script online que promete burlar o\n"
        "licenciamento de um software caro que sua equipe precisa. Você:",
        "alternativas": {
            "a": "Nem pensa nisso e busca alternativas legais.",
            "b": "Testa o script só por curiosidade.",
            "c": "Usa o script para economizar no projeto."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Postura correta! Pirataria nunca é solução.",
            "b": "Curiosidade pode custar caro — evite tentações antiéticas.",
            "c": "Errado! Economizar quebrando a lei não é justificável."
        }
    },
    {
        "pergunta": "⏩ Seu chefe pede para acelerar o projeto,mesmo que\n"
        "precise 'dar um jeitinho' nos testes de segurança. Você:",
        "alternativas": {
            "a": "Explica os riscos e se recusa a pular etapas.",
            "b": "Dá um jeito rápido, prometendo revisar depois.",
            "c": "Pula os testes e entrega logo para agradar."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Corretíssimo! Qualidade e segurança vêm antes de pressa.",
            "b": "Perigoso! Depois pode ser tarde demais para corrigir.",
            "c": "Uma decisão antiética que pode gerar prejuízo enorme."
        }
    },
    {
        "pergunta": "📂 Você está saindo de uma empresa e pensa em copiar o código\n"
        "que desenvolveu lá para usar em projetos futuros. Você:",
        "alternativas": {
            "a": "Sai apenas com seu conhecimento e deixa o código para a empresa.",
            "b": "Copia partes pequenas achando que não fará falta.",
            "c": "Copia tudo, afinal foi você quem escreveu."
        },
        "pontuações": {"a": 1, "b": 0, "c": 0},
        "resposta_certa": "a",
        "comentario": {
            "a": "Parabéns! Ética até o último dia de trabalho.",
            "b": "Ainda é errado; propriedade intelectual não é sua.",
            "c": "Não importa quem escreveu — o código pertence à empresa."
        }
    }
]


def iniciar_dilema(usuarios,email):
    """
    Conduz um questionário com cinco cenários éticos, contabiliza e retorna a pontuação.
    
    Parâmetros:
    usuarios (dict): Dicionário com os usuários cadastrados.
    email (str): Email do usuário cuja pontuação será exibida.
    
    returns: 
    int: pontuacao (total de pontos adquiridos no questionário)
    """
    pontuacao = 0
    print("\n Seja bem-vindo(a) ao CENÁRIOS ÉTICOS!")
    print("Responda aos cinco dilemas com as alternativas (a, b ou c):\n")

    selecionadas = random.sample(PERGUNTAS, k=5)
    
    for i, pergunta in enumerate(selecionadas, 1):     
        print("=" * 75)
        print(f"Cenário {i}: {pergunta['pergunta']}")
        for letra, alternativa in pergunta["alternativas"].items():
            print(f"  ({letra}) {alternativa}")
        print("=" * 75)
        
        while True:
            resposta = input("Digite ('a','b','c') ou 'sair' para encerrar: ").lower()
            match resposta:
                case 'a'| 'b'|'c':
                    break
                case 'sair':    
                    print("Ok. Vamos encerrar por aqui...")
                    return pontuacao
                case _:
                     print("Opção inválida!\n ")   
               
        pontos_resposta = pergunta.get("pontuações", {}).get(resposta, 0)
        pontuacao += pontos_resposta
        
        print(f"\n✅ Você ganhou {pontos_resposta} ponto(s) nesta pergunta.")
        print(pergunta["comentario"][resposta])

        data_resposta = time.strftime("%d - %m - %Y")
        registro = {
            'data': data_resposta,
            'pergunta': pergunta['pergunta'],
            'resposta': resposta,
            'pontos': pontos_resposta
        }
        usuarios[email]['historico_respostas'].append(registro)
        salvar_usuarios(usuarios)



    print(f"\n Você ganhou {pontuacao} ponto(s) nesse dilema!\n")
    return pontuacao
