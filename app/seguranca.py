import bcrypt


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
            hash_ (bytes): Hash armazenado.

        Returns:
            bool: True se corresponder, False caso contrário.
        """
        return bcrypt.checkpw(senha.encode(), hash_)
