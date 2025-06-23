import json
import os
from usuario import (carregar_usuarios,salvar_usuarios,email_valido,
    senha_valida, telefone_valido, cadastrar, alterar_senha,
    editar_conta, recuperar_senha, deletar_conta)
from frases import frase_dia
from dilema import iniciar_dilema
from desafios import desafios_bem


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
          nivel = 'Mestre 👑'
     print(f"\n🚀 Olá, {usuarios[email]['nome']}! Sua jornada pelo BEM+ está em andamento.")
     print("Vamos conferir seu progresso e o impacto positivo que você está construindo...\n")
     print(f"\n⭐ Pontuação total: {pontos} pontos")
     print(f"🔰 Nível atual: {nivel}\n")


# Ranking de Usuários:
def ranking(usuarios):
     """
    Exibe um ranking dos cinco usuários com maior pontuação.
    
    Parâmetros:
     usuarios (dict): Dicionário com os usuários cadastrados.
    
    """
     nome_pontos = []
     for email, dados in usuarios.items():
          nome = dados.get('nome',email)
          pontos = dados.get('pontos',0)
          nome_pontos.append((nome,pontos))
     
     nome_pontos.sort(key=lambda x: x[1], reverse=True)
     top5 = nome_pontos[:5]
     
     print("\n🏆 Top 5 Usuários 🏆\n")
     print(f"{'Pos':<3} {'Nome':<20} {'Pontos':>6}")
     print("=" * 31)

     # Linhas do ranking
     for pos, (nome, pontos) in enumerate(top5, 1):
          print(f"{pos:<3} {nome:<20} {pontos:>6}")

     print("=" * 31)
     
# Menu do usuário:
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
               opcao_usuario = input("Opção: ")
               match opcao_usuario:
                    case '1':
                         print("Então vamos continuar! ")
                         menu_bem(usuarios,email)
                    case '2':
                         email = editar_conta(usuarios,email)
                    case '3':
                         if deletar_conta(usuarios, email):
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
     while True:
          print("\n" + "="*38)
          print(f"🌟 MENU BEM+ - {usuarios[email]['nome']} 🌟".center(38))
          print("="*38)
          print("│ 1 - Frase do Dia                  │")
          print("│ 2 - Iniciar Cenário Ético         │")
          print("│ 3 - Desafios do Bem               │")
          print("│ 4 - Ver Pontuação e Nível         │")
          print("│ 5 - Ver Histórico de Respostas    │")
          print("│ 6 - Ranking de Usuários           │")
          print("│ 0 - Sair do menu BEM+             │")
          print("="*38)          
          opcao_bem = input("Sua opção é? ")
          match opcao_bem:
               case '1':
                    frase_dia()
                    input("\nPressione Enter para continuar...")
               
               case '2':
                    pontos = iniciar_dilema()
                    usuarios[email]['pontos'] += pontos
                    salvar_usuarios(usuarios)
                    
               case '3':
                    desafios_bem(usuarios,email)
                    
               case '4':
                    pontuacao_e_nivel(usuarios,email)
                    input("\nPressione Enter para continuar...")
               
               case '5':
                    print("Desculpe, Histórico de Respostas ainda em manutenção")
                    input("\nPressione Enter para continuar...")
               
               case '6':
                    ranking(usuarios)
                    input("\nPressione Enter para continuar...")
               
               case '0':
                    print("Saindo do Menu BEM+...")
                    input("\nPressione Enter para retornar...")
                    return
               
               case _:
                    print("Opção invalida!")       

          
#Menu inicial:
def menu_inicial():
     """
     Exibe o menu inicial do sistema e direciona para cadastro, login, recuperação de senha ou encerramento.
     """     
     usuarios = carregar_usuarios()
     while True:
          print("\n" + "="*32)
          print("📘  MENU INICIAL - BEM+  📘".center(32))
          print("="*32)
          print("│ 1 - Cadastrar               │")
          print("│ 2 - Login                   │")
          print("│ 3 - Recuperação de senha    │")
          print("│ 4 - Sair                    │")
          print("="*32)
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


menu_inicial()                                  