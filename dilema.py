import os
import json
import random
import time
import textwrap
from utils import Utils
from repo_usuario import RepoUsuario


DILEMA = os.path.join('dados', 'dilema.json')

class Dilema:
    
    def __init__(self, repo: RepoUsuario, caminho = DILEMA):
        self.users = repo
        self.caminho = caminho

        try:
            with open(self.caminho, "r", encoding="utf-8") as arq:
                self.perguntas = json.load(arq)

        except FileNotFoundError:
            self.perguntas = []
            


    # Iniciar cenários éticos:
    def executar_dilema(self, email):
        """
        Conduz um questionário com cinco cenários éticos, contabiliza e retorna a pontuação.
        
        Parâmetros:
            email (str): email do usuário atualmente logado.
            
        return: 
            int: pontuacao (total de pontos adquiridos no questionário)
        """
        user = self.users.buscar(email)
        pontuacao = 0
        Utils.limpar_tela()
        print("\n Seja bem-vindo(a) ao CENÁRIOS ÉTICOS!")
        print("Responda aos cinco dilemas com as alternativas (a, b ou c):\n")

        selecionadas = random.sample(self.perguntas, k=5)
        
        # looping de perguntas:
        for i, pergunta in enumerate(selecionadas, 1):     
            Utils.limpar_tela()
            print("=" * 75)
            
            # formatar para largura maxima = 70:
            txt_formatado = textwrap.fill(pergunta['pergunta'],width=70)
            print(f"Cenário {i}: ")
            print(txt_formatado)
            for letra, alternativa in pergunta["alternativas"].items():
                alt_formatada = textwrap.fill(alternativa, width=66)
                alt_indentada = textwrap.indent(alt_formatada, prefix="    ")
                print(f"({letra}) {alt_indentada.strip()}")
            print("=" * 75)
            
            while True:
                resposta = Utils.nao_vazio("Digite ('a','b','c') ou 'sair' para encerrar: ").lower()
                match resposta:
                    case 'a'| 'b'|'c':
                        break
                    case 'sair':    
                        print("Ok. Vamos encerrar por aqui...")
                        self.users.salvar_usuarios()
                        return pontuacao
                    case _:
                        print("Opção inválida!\n ")   
                
            pontos_resposta = pergunta.get("pontuações", {}).get(resposta, 0)
            pontuacao += pontos_resposta
            
            print(f"\n✅ Você ganhou {pontos_resposta} ponto(s) nesta pergunta.")
            print(pergunta["comentario"][resposta])
            input("pressione Enter para continuar...")

            data_resposta = time.strftime("%d/%m/%Y")
            registro = {
                'data': data_resposta,
                'pergunta': pergunta['pergunta'],
                'resposta': resposta,
                'pontos': pontos_resposta
            }
            user.historico_respostas.append(registro)

        self.users.salvar_usuarios()
        print(f"\n Você ganhou {pontuacao} ponto(s) nesse dilema!\n")
        return pontuacao

