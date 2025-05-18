import json
import os
from frases import frase_dia
from dilema import iniciar_dilema
from desafios import desafios_bem

arquivo_usuarios = os.path.join('dados', 'usuarios.json')

#Carregamento de dados já existentes:
def carregar_usuarios():
     """
     Carrega os usuários do arquivo JSON, se existir.

     Retorna:
     dict: Dicionário com os dados dos usuários cadastrados.
     """
     if os.path.exists(arquivo_usuarios):
          with open(arquivo_usuarios,'r') as arquivo:
               return json.load(arquivo)
     return {}

#Salvar usuario:         
def salvar_usuarios(usuarios):  
     """
     Salva os dados dos usuários no arquivo usuarios.JSON.

     Parâmetros:
     usuarios (dict): Dicionário contendo os dados dos usuários.
     """
     with open(arquivo_usuarios,'w') as arquivo:
          json.dump(usuarios, arquivo, indent=4)

#Validação de email
def email_valido(email):  
     """
     Verifica se o e-mail é válido de acordo com domínios permitidos.

     Parâmetros:
     email (str): E-mail informado pelo usuário.

     Retorna:
     bool: True se o e-mail for válido, False caso contrário.
     """
     return email.endswith('@gmail.com') or email.endswith('@ufrpe.br') or email.endswith('@hotmail.com') or email.endswith('@outlook.com')

#Validação de senha
def senha_valida(senha):
     """
     Verifica se a senha contém apenas dígitos e tem 6 caracteres.

     Parâmetros:
     senha (str): Senha informada pelo usuário.

     Retorna:
     bool: True se a senha for válida, False caso contrário.
     """
     return senha.isdigit() and len(senha) == 6

#Cadastro de usuário:
def cadastrar(usuarios):
     """
     Realiza o cadastro de um novo usuário com nome, telefone, email, senha e pergunta secreta.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários existentes.
     """ 
     nome = input("Digite seu nome: ")
     telefone = input("Digite seu telefone com 11 digitos: Ex:81999998888 ")
     while not telefone.isdigit() or len(telefone) != 11:
          print("Erro de digitação!")
          telefone = input(" Tente novamente apenas os numeros (DDD + numeros: ex 71988889999): ")
     
     email = input("Digite seu email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ").lower()
     if not email_valido(email):
          print("email invalido. Tente novamente!")
          return

     if email in usuarios:
          print("email já cadastrado. ")
          return           
     
     senha = input("Digite uma senha com 6 digitos (apenas números): ")
     if not senha_valida(senha):
          print("Senha inválida! Tente novamente digitando apenas números.")
          return
     
     print("\n Para recuperação de senha, responda a seguinte pergunta: ")   
     resposta_secreta = input("Qual o nome da sua professora favorita? ").strip()
     while resposta_secreta == "":
          resposta_secreta = input("Por favor, digite um nome válido: ").strip()
               
     usuarios[email] = {
          'nome' : nome,
          'telefone' : telefone,
          'senha' : senha,
          'pontos' : 0,
          'resposta_secreta' : resposta_secreta
     }
     
     salvar_usuarios(usuarios)
     print("Cadastro realizado com sucesso!")

def alterar_senha(usuarios, email):
    """
    Permite ao usuário alterar a senha, sendo necessário a confirmação da senha anterior.

    Parâmetros:
    usuarios (dict): Dicionário com os usuários cadastrados.
    email (str): Email do usuário que deseja alterar a senha.
    """
    senha_atual = input("Digite sua senha atual (6 dígitos) para confirmar a alteração: ")
    if senha_atual != usuarios[email]['senha']:
        print("❌ Senha atual incorreta! Voltando ao menu...")
        return
    
    nova_senha = input("Digite sua nova senha composta por 6 números: ")
    while not senha_valida(nova_senha):
        nova_senha = input("Senha inválida. Tente novamente com 6 dígitos numéricos: ")

    usuarios[email]['senha'] = nova_senha
    salvar_usuarios(usuarios)
    print("✅ Senha atualizada com sucesso!")
    
#Editar usuario:
def editar_conta(usuarios,email):
     """
     Permite ao usuário editar suas informações pessoais, incluindo email, nome, telefone, senha e resposta secreta.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     email (str): Email do usuário que deseja editar.
     """
     print("Dados atuais:")
     print(f"Email: {email}")
     print(f"Nome: {usuarios[email]['nome']}")
     print(f"Telefone: {usuarios[email]['telefone']}")
     while True:
          print("O que deseja editar: ")
          print("1 - email")
          print("2 - nome")
          print("3 - telefone")
          print("4 - senha")
          print("5 - Resposta_secreta")
          print("6 - sair")
          editar = input("opção: ")
          match editar:
               case '1': #Editar Email
                    novo_email = input("Digite seu novo email (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com): ")
                    while not email_valido(novo_email):
                         novo_email = input("Email inválido ou já existente! Tente novamente (@ufrpe.br, @gmail.com, @hotmail.com ou @outlook.com)")               
                    usuarios[novo_email] = usuarios[email]
                    del usuarios[email]
                    salvar_usuarios(usuarios)
                    print("email atualizado com sucesso!")
                    email = novo_email
                    
               case '2':
                    novo_nome = input("Digite o novo nome: ")
                    usuarios[email]['nome'] = novo_nome
                    salvar_usuarios(usuarios)
                    print("Nome atualizado com sucesso!")
                    
               case '3':
                    novo_tel = input("Digite o novo número de telefone: ")
                    while not novo_tel.isdigit() or len(novo_tel) != 11:
                         novo_tel = input("Número inválido. Tente com 11 digitos e apenas os números")
                    usuarios[email]['telefone'] = novo_tel
                    salvar_usuarios(usuarios)
                    print("Telefone atualizado com sucesso!")
                    
               case '4':
                    alterar_senha(usuarios,email)
                    
               case '5':
                    print("Responda a seguinte pergunta novamente: ")
                    resposta_secreta = input("Qual o nome da sua professora favorita? ").strip()
                    while resposta_secreta == "":
                         resposta_secreta = input("Por favor, digite um nome válido: ").strip()
                    usuarios[email]['resposta_secreta'] = resposta_secreta
                    salvar_usuarios(usuarios)
                    print("Nova resposta secreta salva com sucesso! ")
                    
               case '6':
                    print("Vamos voltar então...")
                    break
               case _:
                    print("Opção inválida!")     

#Recuperar senha:
def recuperar_senha(usuarios):
     """
     Permite ao usuário recuperar a senha caso tenha esquecido, mediante verificação de email,
     telefone e resposta secreta.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     email (str): Email do usuário que deseja recuperar a conta.
     """
     email = input("Digite seu email cadastrado: ").lower()
     
     if email not in usuarios:
          print("Email não cadastrado!")
          return
     
     telefone = input("Digite seu telefone com 11 digitos: Ex:81999998888 ")
     while not telefone.isdigit() or len(telefone) != 11:
          print("Erro de digitação!")
          telefone = input(" Tente novamente apenas os numeros (DDD + numeros: ex 71988889999): ")
     
     if telefone != (usuarios[email]['telefone']):
          print("Telefone não correspondente!")
          return
     
     print("Responda a seguinte pergunta secreta cadastrada:")
     resposta_secreta = input("Qual o nome da sua professora preferida? ")
     if resposta_secreta.lower() != usuarios[email]['resposta_secreta'].lower():
          print("Resposta secreta incorreta!")
          return
     
     alterar_senha(usuarios,email)
     
#Deletar usuario:
def deletar_conta(usuarios,email):
     """
     Exclui a conta do usuário após confirmação da intenção e validação da senha.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     email (str): Email do usuário que deseja excluir a conta.

     Retorna:
     bool: True se a conta foi excluída com sucesso, False caso contrário.
     """
     confirmacao = input("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
     if confirmacao == 's':
          confirmacao_senha = input("Para excluir sua conta, confirme sua senha: ")
          if confirmacao_senha == usuarios[email]['senha']:
               del usuarios[email]
               salvar_usuarios(usuarios)
               print("Sua conta foi deletada com sucesso.")
               return True
          else:
               print("Senha incorreta!")
               return False
     else:
          print("Operação cancelada!")
          return False     

#Ver pontuação e nível:
def pontuacao_e_nivel(usuarios, email):
     """
     Exibe, com uma saudação personalizada, a pontuação e
     o nível do usuário com base nos pontos acumulados.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     email (str): Email do usuário cuja pontuação será exibida.
     """
     pontos = usuarios[email]['pontos']
     if pontos < 10:
          nivel = 'Iniciante 🐣'
     elif pontos < 40:
          nivel = 'Explorador 🌱'
     elif pontos < 70:
          nivel = 'Consciente 💡'
     elif pontos < 90:
          nivel = 'Mentor 🌟'
     else:
          nivel = 'Mestre 🌈'
     print(f"\n🚀 Olá, {usuarios[email]['nome']}! Sua jornada pelo BEM+ está em andamento.")
     print("Vamos conferir seu progresso e o impacto positivo que você está construindo...\n")
     print(f"\n⭐ Pontuação total: {pontos} pontos")
     print(f"🔰 Nível atual: {nivel}\n")

#Logar:
def login(usuarios):
     """
     Realiza o login de um usuário e apresenta opções para acessar o menu BEM+,
     editar conta, deletar conta ou sair.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     """
     email = input("Digite seu email: ").lower()
     senha = input("Digite sua senha: ")
     
     if email in usuarios and usuarios[email]['senha'] == senha:
          print(f"\nBem-vindo(a), {usuarios[email]['nome']}")
          while True:
               print("O que deseja fazer? ")
               print("1 - Prosseguir para o Menu BEM+")
               print("2 - Editar Conta")
               print("3 - Deletar Conta")
               print("4 - Sair")
               opcaoUsuario = input("Opção: ")
               match opcaoUsuario:
                    case '1':
                         print("Então vamos continuar! ")
                         menu_bem(usuarios,email)
                    case '2':
                         editar_conta(usuarios,email)
                         return
                    case '3':
                         deletar_conta(usuarios, email)
                         break
                    case '4':
                         print("Até mais então...")
                         break
                    case _:
                         print("opção inválida")          
     else:
          print("Email ou senha inválidos. ")

#Menu BEM+:
def menu_bem(usuarios,email):
     """
     Apresenta o menu principal do BEM+ com as opções de funcionalidades ao usuário.

     Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
     email (str): Email do usuário logado.
     """     
     print(f"O que faremos hoje {usuarios[email]['nome']}? ")
     print("[1] Frase do Dia")
     print("[2] Iniciar um Cenário Ético")
     print("[3] Receber um Desafio do Bem")
     print("[4] Ver Pontuação e Nível")
     print("[5] Ver Histórico de Respostas")
     print("[6] Ranking de Usuários")
     print("[7] Sair")
     opcaoBem = input("Opção: ")          
     
     match opcaoBem:
          case '1':
               frase_dia()
          
          case '2':
               pontos = iniciar_dilema()
               usuarios[email]['pontos'] = usuarios[email].get('pontos', 0) + pontos
               salvar_usuarios(usuarios)
               
          case '3':
               desafios_bem(usuarios,email)
               salvar_usuarios(usuarios)
               
          case '4':
               pontuacao_e_nivel(usuarios,email)
               
          case '5':
               print("Em manutenção")
               
          case '6':
               print("Em manutenção")
               
          case '7':
               print("Em manutenção")
               
          case _:
               print("Opção invalida!")       
     
#Menu principal:
def menu():
     """
     Exibe o menu principal do sistema e direciona para cadastro, login, recuperação de senha ou encerramento.
     """     
     usuarios = carregar_usuarios()
     while True:
        print("1 - Cadastrar")
        print("2 - Login")
        print("3 - Recuperação de senha")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")
        
        match opcao:
             case '1':
                  cadastrar(usuarios)
             case '2':
                  login(usuarios)
             case '3':
                  recuperar_senha(usuarios)
             case '4':
                  print("Até mais então...")
                  break
             case _:
                  print("opção inválida")                  

menu()                                  