import os


class Utils:
    """Funções utilitárias de terminal. """
    
    def naoVazio(mensagem):
        """
        Solicita uma entrada não vazia ao usuário.
        Exibe a mensagem até que uma entrada válida (não vazia) seja fornecida.

        Args:
            mensagem (str): Texto exibido ao usuário no prompt.

        Returns:
            str: Texto digitado pelo usuário, sem espaços extras.
        """
        while True:
            if texto := input(mensagem).strip():   #walrus 
                return texto
            print("Entrada vazia. Tente novamente.\n")

    @staticmethod
    def limparTela():
        """
        Limpa o terminal da forma apropriada para o sistema operacional.

        Usa 'cls' no Windows e 'clear' no Linux/macOS.
        """
        comando = 'cls' if os.name == 'nt' else 'clear'
        os.system(comando)
