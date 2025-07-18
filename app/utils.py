import os
import bcrypt


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


class SenhaCripto:
    """
    Encapsula o hashing e verificação de senhas com bcrypt.
    """

    @staticmethod
    def hashSenha(senha) -> bytes:
        """
        Gera um hash bcrypt para a senha informada.

        Args:
            senha (str): Senha em texto puro.

        Returns:
            bytes: Hash seguro (com salt incorporado).
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode(), salt)

    @staticmethod
    def verificarSenha(senha, hash_: bytes) -> bool:
        """
        Verifica se a senha confere com o hash armazenado.

        Args:
            senha (str): Senha em texto puro.
            hash (bytes): Hash armazenado.

        Returns:
            bool: True se corresponder, False caso contrário.
        """
        return bcrypt.checkpw(senha.encode(), hash_)
