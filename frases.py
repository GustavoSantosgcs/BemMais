import random

frases = [
    
    "A gentileza é a linguagem que o surdo pode ouvir e o cego pode ver.",
    "O mundo muda com seu exemplo, não com sua opinião.",
    "Seja a mudança que você quer ver no mundo.",
    "Uma atitude positiva é o primeiro passo para o sucesso.",
    "Cada pequeno ato de bondade conta.",
    "O bem que você faz hoje será sua força amanhã."
          
]

def frase_dia():
     print("\n✨Frase do dia ✨")
     print(random.choices(frases))