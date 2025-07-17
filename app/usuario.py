import re


class Usuario:         
     """
     Representa um usuário do sistema BEM+.

     Armazena dados pessoais, autenticação, pontuação e histórico de interações.
     Fornece métodos para validação, alteração e serialização.
     """
     
     def __init__(self, nome, telefone, email, senha, pontos=0, resposta_secreta=None,
                     desafios_realizados=None, historico_respostas=None):
          """
          Inicializa um novo usuário com validações de entrada.

          Args:
               nome (str): Nome do usuário.
               telefone (str): Telefone com DDD.
               email (str): Email válido (@ufrpe.br, @gmail.com etc).
               senha (str): Senha numérica de 6 dígitos.
               pontos (int): Pontuação inicial (default = 0).
               resposta_secreta (str | None): Resposta secreta para recuperação de senha.
               desafios_realizados (list | None): Lista de desafios concluídos.
               historico_respostas (list | None): Histórico de respostas éticas.

          Raises:
               ValueError: Se algum dado for inválido.
          """
          
          if not self.emailValido(email):
               raise ValueError("Email digitado é inválido.")
          if not self.senhaValida(senha):
               raise ValueError("Senha digitada é inválida")
          if not self.telefoneValido(telefone):
               raise ValueError("Telefone digitado é inválido!")                    
                    
          self.nome = nome
          self.telefone = telefone
          self.email = email
          self.senha = senha
          self.pontos = pontos
          self.resposta_secreta = resposta_secreta
          self.desafios_realizados = list(desafios_realizados) if desafios_realizados is not None else []
          self.historico_respostas = list(historico_respostas) if historico_respostas is not None else []

     # Serialização:
     def toDict(self):
          """
          Converte o objeto Usuario em um dicionário compatível com JSON.

          Returns:
               dict: Representação serializável do usuário.
          """
          return {
               "nome": self.nome,
               "telefone": self.telefone,
               "email": self.email,
               "senha": self.senha,
               "pontos": self.pontos,
               "resposta_secreta": self.resposta_secreta,
               "desafios_realizados": self.desafios_realizados,
               "historico_respostas": self.historico_respostas,
          }
               
     # Deserialização:           
     @classmethod
     def fromDict(cls, dados):
          """Cria um Usuario a partir de um dicionário (caminho inverso do toDict)."""
          return cls(**dados) # '**' espalha as chaves/valores como argumentos nomeados para o __init__. 

     # Validação de telefone:
     @staticmethod
     def telefoneValido(telefone):
          """
          Verifica se o telefone informado está no formato brasileiro válido.
          Exemplo válido: (81) 98877-4422 ou (81)98877-4422

          Args:
               telefone (str): Telefone informado.

          Returns:
               bool: True se válido, False caso contrário.
          """
          padrao = r'^\([1-9]{2}\)\s?9[0-9]{4}-[0-9]{4}$'
          return re.match(padrao,telefone) is not None

     # Validação de email:
     @staticmethod
     def emailValido(email):
          """
          Verifica se o email possui um formato válido e pertence a um domínio permitido.

          Args:
               email (str): Email informado pelo usuário.

          Returns:
               bool: True se o email for válido, False caso contrário.
          """
          padrao = r'^[\w\.-]+@(?:gmail\.com|hotmail\.com|outlook\.com|ufrpe\.br)$'
          return re.match(padrao, email) is not None
            
     # Validação de senha:
     @staticmethod
     def senhaValida(senha):
          """
          Verifica se a senha contém apenas dígitos e tem 6 caracteres.

          Args:
               senha (str): Senha informada pelo usuário.

          Returns:
               bool: True se a senha for válida, False caso contrário.
          """
          return senha.isdigit() and len(senha) == 6

     # Alterar email:
     def alterarEmail(self, novo_email):
          """
          Atualiza o email do usuário após validação.

          Args:
               novo_email (str): Novo email digitado pelo usuário.

          Raises:
               ValueError: Se o email não for válido.
          """
          if not Usuario.emailValido(novo_email):
               raise ValueError("Formato de email inválido!")
          self.email = novo_email

     # Alteração de senha:
     def alterarSenha(self, senha_atual, nova_senha):
          """
           Atualiza a senha do usuário, conferindo a senha atual.
          
          Args:
               senha_atual (str): senha atual do usuário para autenticação.
               nova_senha (str): nova senha numérica de exatamente 6 dígitos.

          Raises:
               ValueError: se a senha atual não confere ou nova senha for inválida.
          """
          if senha_atual != self.senha:
               raise ValueError("Senha atual incorreta.")
          
          if not self.senhaValida(nova_senha):
               raise ValueError("Nova senha inválida (seis dígitos numéricos).")
          self.senha = nova_senha

     # Alterar resposta secreta:
     def alterarResposta(self, nova_resposta):
          """
          Atualiza a resposta secreta do usuário.

          Args:
               nova_resposta (str): Nova resposta.

          Raises:
               ValueError: Se a nova resposta for vazia.
          """
          
          self.resposta_secreta = nova_resposta
          

