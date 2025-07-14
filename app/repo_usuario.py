import json
import os
from .usuario import Usuario


CAMINHO = os.path.join('dados', 'usuarios.json')

class RepoUsuario:
     """ Carrega, salva e gerencia todos os objetos do Usuario."""
     
     def __init__(self):
          """
          Inicializa o repositório de usuários em memória.

          Carrega os dados do arquivo JSON (CAMINHO) para o dicionário interno
          self.usuarios. Se o arquivo não existir ou estiver corrompido,
          inicia com base vazia.
          """
          self.usuarios = self.carregarUsuarios()
          
     
     # Carregar usuários:
     def carregarUsuarios(self): 
        """Lê o JSON (se existir) e devolve dict de objetos Usuario."""
        if os.path.exists(CAMINHO):
            try:
                with open(CAMINHO, "r", encoding="utf-8") as arq:
                    arq_bruto = json.load(arq)
                    return {key_email: Usuario.fromDict(d) for key_email, d in arq_bruto.items()}
            except (json.JSONDecodeError, IOError):
                print("⚠️ Erro ao ler arquivo JSON. Iniciando base vazia.")
        return {}
   
   
     # Salvar usuários:
     def salvarUsuarios(self):
          """Serializa o dicionário em memória para o JSON."""
          os.makedirs(os.path.dirname(CAMINHO), exist_ok=True)
          arq_bruto = {}
          for key_email, user in self.usuarios.items():
               dicio_do_usuario = user.toDict()
               arq_bruto[key_email] = dicio_do_usuario
               
          with open(CAMINHO, "w", encoding="utf-8") as arq:
               json.dump(arq_bruto, arq, indent=4, ensure_ascii=False)


     # Método cadastrar:
     def cadastrar(self, usuario):
          if usuario.email in self.usuarios:
               raise ValueError("Email já cadastrado.")
          self.usuarios[usuario.email] = usuario
          self.salvarUsuarios()


     # Buscar usuários:
     def buscar(self, email):
          """
          Busca um usuário pelo email.

          Parâmetros:
               email (str): email do usuário a ser pesquisado.

          Retorna:
               Usuario: instância encontrada, ou None se não existir.
          """
          return self.usuarios.get(email)


     # Listar usuários:
     def listar(self):
          """
          Retorna todos os usuários cadastrados.

          Retorna:
               list[Usuario]: lista com todos os objetos Usuario do repositório.
          """
          return list(self.usuarios.values())


     # Remover usuários:
     def remover(self, email):
          """
          Remove o usuário identificado pelo email do repositório e atualiza o JSON.

          Parâmetros:
               email (str): email do usuário a ser removido.
          """
          if email in self.usuarios:
               del self.usuarios[email]
               self.salvarUsuarios()


     # Atualizar email (método):
     def atualizarEmail(self, email, novo_email):
          """
          Atualiza a chave do usuário de email para novo_email e persiste.

          Parâmetros:
               email (str): email atual do usuário.
               novo_email (str): novo email a ser atribuído.

          Raise:
               ValueError: se novo_email já estiver cadastrado ou email não existir.
          """
          
          if novo_email in self.usuarios:
               raise ValueError("Novo email digitado já está cadastrado.")
          usuario = self.usuarios.pop(email)
          usuario.email = novo_email
          self.usuarios[novo_email] = usuario
          self.salvarUsuarios()
