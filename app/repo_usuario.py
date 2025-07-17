import json
import os
from .usuario import Usuario


CAMINHO = os.path.join('dados', 'usuarios.json')

class RepoUsuario:
     """
     Repositório responsável por gerenciar os objetos da classe Usuario.

     Permite carregar, salvar, buscar, remover e atualizar usuários
     armazenados em arquivo JSON.
     """
     
     def __init__(self):
          """
          Inicializa o repositório, carregando usuários do JSON ou iniciando base vazia.
          """
          
          self.usuarios = self.carregarUsuarios()
            
     def carregarUsuarios(self): 
          """
          Lê o arquivo JSON de usuários e converte em objetos Usuario.

          Returns:
               dict: Mapeamento email -> Usuario.
          """
          if os.path.exists(CAMINHO):
               try:
                    with open(CAMINHO, "r", encoding="utf-8") as arq:
                         arq_bruto = json.load(arq)
                    return {key_email: Usuario.fromDict(d) for key_email, d in arq_bruto.items()}
               except (json.JSONDecodeError, IOError):
                    print("⚠️ Erro ao ler arquivo JSON. Iniciando base vazia.")
          return {}
  
     def salvarUsuarios(self):
          """Serializa o dicionário em memória para o JSON."""
          
          os.makedirs(os.path.dirname(CAMINHO), exist_ok=True)
          arq_bruto = {}
          for key_email, user in self.usuarios.items():
               dicio_do_usuario = user.toDict()
               arq_bruto[key_email] = dicio_do_usuario
               
          with open(CAMINHO, "w", encoding="utf-8") as arq:
               json.dump(arq_bruto, arq, indent=4, ensure_ascii=False)

     def cadastrar(self, usuario):
          """
          Adiciona um novo usuário ao repositório e persiste no JSON.
         
          Args:
               usuario (Usuario): Usuário a ser cadastrado.
         
          Raises:
               ValueError: Se o email já estiver cadastrado.
          """     
          
          if usuario.email in self.usuarios:
               raise ValueError("Email já cadastrado.")
          self.usuarios[usuario.email] = usuario
          self.salvarUsuarios()

     def buscar(self, email):
          """
          Busca um usuário pelo email.
          
          Args:
               email (str): Email do usuário a ser pesquisado.
          
          Returns:
               Usuario | None: Instância do usuário encontrado ou None se não existir.
          """
          
          return self.usuarios.get(email)

     def listar(self):
          """
          Retorna todos os usuários cadastrados.

          Returns:
               list[Usuario]: lista com todos os objetos Usuario do repositório.
          """
          return list(self.usuarios.values())

     def remover(self, email):
          """
          Remove o usuário identificado pelo email do repositório e atualiza o JSON.

          Args:
               email (str): email do usuário a ser removido.
          """
          if email in self.usuarios:
               del self.usuarios[email]
               self.salvarUsuarios()

     # Atualizar email (método):
     def atualizarEmail(self, email, novo_email):
          """
          Atualiza o email de um usuário no repositório e persiste a alteração.

          Args:
               email (str): Email atual do usuário.
               novo_email (str): Novo email a ser atribuído.

          Raises:
               ValueError: Se o novo_email já estiver em uso.
          """
          
          if novo_email in self.usuarios:
               raise ValueError("Novo email digitado já está cadastrado.")
          usuario = self.usuarios.pop(email)
          usuario.email = novo_email
          self.usuarios[novo_email] = usuario
          self.salvarUsuarios()
