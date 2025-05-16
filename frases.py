import random

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

def frase_dia():
    frase = random.choice(frases)
    borda = "=" * (len(frase) + 4)
    print("\n✨ Frase do Dia ✨")
    print(borda)
    print(f"| {frase} |")
    print(borda)
