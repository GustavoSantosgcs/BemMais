import json
import os
import random
import time

# Lista de frases
frases = [
    "A tecnologia é melhor quando une as pessoas em vez de separá-las. - Autor Desconhecido",
    "A verdade pode ser encontrada em um único lugar: o código. - Robert C. Martin",
    "Simplicidade é o último grau de sofisticação. - Leonardo da Vinci",
    "Medir o progresso por linhas de código é como medir a construção de aviões pelo peso. - Bill Gates",
    "A inovação distingue um líder de um seguidor. - Steve Jobs",
    "Primeiro resolva o problema. Depois, escreva o código. - John Johnson",
    "Qualquer tolo escreve código que um computador entende. Bons programadores escrevem código que humanos entendem. - Martin Fowler",
    "Programar é pensar, não digitar. - Autor Desconhecido",
    "Não se preocupe se não funcionar direito. Se tudo desse certo, você estaria sem emprego. - Mosher's Law",
    "Existem 10 tipos de pessoas: as que entendem binário e as que não. - Piada Nerd",
    "A função do bom software é fazer o complexo parecer simples. - Grady Booch",
    "Não documente o problema, corrija-o. - Atli Björgvinsson",
    "Aquele que move montanhas começa carregando pequenas pedras. - Confúcio",
    "O sucesso é a soma de pequenos esforços repetidos dia após dia. - Robert Collier"
]


ARQUIVO_FRASE = os.path.join('dados','frase_dia.json')

def frase_dia():
    """
    Exibe a frase do dia, garantindo que a mesma frase seja mantida até o dia seguinte usando o
    módulo Time.
    
    Verifica também se já existe uma frase armazenada para a data atual no arquivo 'frase_dia.json'.
    """
    hoje = time.strftime("%d -%m - %Y")

    # Verificação se já existe uma frase salva para o dia atual
    if os.path.exists(ARQUIVO_FRASE):
        with open(ARQUIVO_FRASE, 'r',encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if dados.get("data") == hoje:
            frase = dados["frase"]
        else:
            frase = random.choice(frases)
            with open(ARQUIVO_FRASE, 'w',encoding="utf-8") as arquivo:
                json.dump({"data": hoje, "frase": frase}, arquivo, indent=4)
    else:
        frase = random.choice(frases)
        with open(ARQUIVO_FRASE, 'w',encoding="utf-8") as arquivo:
            json.dump({"data": hoje, "frase": frase}, arquivo, indent=4)

    borda = "=" * (len(frase) + 4)
    print("\n✨ Frase do Dia ✨")
    print(borda)
    print(f"| {frase} |")
    print(borda)
