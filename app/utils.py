import os

class Utils:
    """Funções utilitárias de terminal. """
    
    def naoVazio(mensagem):
        """Looping até o usuário digitar algo diferente de vazio."""
        while True:
            if texto := input(mensagem).strip():   #walrus 
                return texto.strip()
            print("Entrada vazia. Tente novamente.\n")


    def limparTela():
        """Limpa o terminal."""
        comando = 'cls' if os.name == 'nt' else 'clear'
        os.system(comando)