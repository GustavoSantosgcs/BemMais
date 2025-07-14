import re


# Classe usuário:
class Usuario:         
     def __init__(self, nome, telefone, email, senha, pontos=0, resposta_secreta=None,
                     desafios_realizados=None, historico_respostas=None):
          """
          Constrói um novo usuário e vlaida seus daados iniciais.

          Parâmetros:
               nome (str).
               telefone (str).
               email (str): email válido (@ufrpe.br, @gmail.com, etc.).
               senha (str): senha numérica de 6 dígitos.
               pontos (int): pontuação inicial (default=0).
               resposta_secreta (str|None): resposta para recuperação de senha.
               desafios_realizados (list|None): lista inicial de códigos de desafios.
               historico_respostas (list|None): lista inicial de respostas.

          Raise:
          ValueError: se qualquer dado de entrada não passar nas validações.
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
               """Converte o objeto para um dicionário JSON."""
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
          Verifica se o telefone informado possui um formato padrão do Brasil.
          Aceita o número com o sem espaço após o DDD
          Ex.:(81) 98877-4422 ou (81)98877-4422
          
          Parâmetros:
               telefone (str): telefone informado pelo usuário.
          
          Retorna:
               bool: True se o telefone estiver valido, False caso negativo.
          """
          padrao = r'^\([1-9]{2}\)\s?9[0-9]{4}-[0-9]{4}$'
          return re.match(padrao,telefone) is not None


     # Validação de email:
     @staticmethod
     def emailValido(email):
          """
          Verifica se o email possui um formato válido e pertence a um domínio permitido.

          Parâmetros:
               email (str): Email informado pelo usuário.

          Retorna:
               bool: True se o email for válido, False caso contrário.
          """
          padrao = r'^[\w\.-]+@(?:gmail\.com|hotmail\.com|outlook\.com|ufrpe\.br)$'
          return re.match(padrao, email) is not None
      
          
     # Validação de senha:
     @staticmethod
     def senhaValida(senha):
          """
          Verifica se a senha contém apenas dígitos e tem 6 caracteres.

          Parâmetros:
          senha (str): Senha informada pelo usuário.

          Retorna:
          bool: True se a senha for válida, False caso contrário.
          """
          return senha.isdigit() and len(senha) == 6


     # Alterar email:
     def alterarEmail(self, novo_email):
          """
          Altera o email do usuário após validar seu formato.

          Parâmetros:
               novo_email (str): novo endereço de email a ser atribuído.
          
          Raise:
               ValueError: Se o novo_email não corresponder ao padrão válido.
          """
          if not Usuario.emailValido(novo_email):
               raise ValueError("Formato de email inválido!")
          self.email = novo_email


     # Alteração de senha:
     def alterarSenha(self, senha_atual, nova_senha):
          """
           Atualiza a senha do usuário, conferindo a senha atual.
          
          Parâmetros:
               senha_atual (str): senha atual do usuário para autenticação.
               nova_senha (str): nova senha numérica de exatamente 6 dígitos.

          Raise:
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
          Atualiza a resposta secreta do usuário para recuperação de senha.

          Parâmetros:
               nova_resposta (str): Nova resposta não vazia.

          Raise:
               ValueError: Se nova_resposta for vazia.
          """
          self.resposta_secreta = nova_resposta
          

