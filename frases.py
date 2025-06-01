import json
import os
import random
import time

frases = [
    "A gentileza é a linguagem que o surdo pode ouvir e o cego pode ver. - Mark Twain",
    "O mundo muda com seu exemplo, não com sua opinião. - Paulo Freire",
    "Seja a mudança que você quer ver no mundo. - Mahatma Gandhi",
    "Uma atitude positiva é o primeiro passo para o sucesso. - Autor desconhecido",
    "Cada pequeno ato de bondade conta. - Dalai Lama",
    "O bem que você faz hoje será sua força amanhã. - Autor desconhecido",
    "A tecnologia move o mundo. - Steve Jobs",
    "Ética em TI é tão vital quanto código limpo. - Desconhecido"
]

arquivo_frase = os.path.join('dados','frase_dia.json')

def frase_dia():
    """
    Exibe a frase do dia, garantindo que a mesma frase seja mantida até o dia seguinte usando o
    módulo Time.
    
    Verifica também se já existe uma frase armazenada para a data atual no arquivo 'frase_dia.json'.
    """
    hoje = time.strftime("%d-$m-%Y")

    # Verificação se já existe uma frase salva para o dia atual
    if os.path.exists(arquivo_frase):
        with open(arquivo_frase, 'r') as arquivo:
            dados = json.load(arquivo)
        if dados.get("data") == hoje:
            frase = dados["frase"]
        else:
            frase = random.choice(frases)
            with open(arquivo_frase, 'w') as arquivo:
                json.dump({"data": hoje, "frase": frase}, arquivo, indent=4)
    else:
        frase = random.choice(frases)
        with open(arquivo_frase, 'w') as arquivo:
            json.dump({"data": hoje, "frase": frase}, arquivo, indent=4)

    borda = "=" * (len(frase) + 4)
    print("\n✨ Frase do Dia ✨")
    print(borda)
    print(f"| {frase} |")
    print(borda)
