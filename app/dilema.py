import os
import json
import random
import time
from .utils import Utils
from .repo_usuario import RepoUsuario
from .ui import Ui
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule


DILEMA = os.path.join('dados', 'dilema.json')

class Dilema:
    """
    Gerencia o quiz de cenários éticos do BEM+.

    Carrega cenários de um JSON, conduz o questionário com 5 perguntas,
    contabiliza pontos, registra histórico de respostas e salva o usuário.
    """
    
    def __init__(self, repo: RepoUsuario, caminho=DILEMA):
        """
        Inicializa o gerenciador de dilemas éticos.

        Carrega perguntas de um arquivo JSON e mantém o repositório de usuários.

        Parâmetros:
            repo (RepoUsuario): Repositório para buscar e salvar usuários.
            caminho (str): Caminho para o arquivo JSON de cenários éticos.
        """
        
        self.ui = Ui()
        self.users = repo
        self.caminho = caminho

        try:
            with open(self.caminho, "r", encoding="utf-8") as arq:
                self.perguntas = json.load(arq)

        except FileNotFoundError:
            self.perguntas = [] 

    def executarDilema(self, email):
        """
        Executa o quiz de 5 cenários éticos e retorna os pontos obtidos.

        O usuário pode digitar 'sair' a qualquer momento para encerrar
        antecipadamente, sem perder a pontuação adquirida .

        Args:
            email (str): Email do usuário logado.

        Returns:
            int: Total de pontos conquistados no questionário.
        """
        
        user = self.users.buscar(email)
        pontuacao = 0
        Utils.limparTela()
        self.ui.tituloDaFuncRich("Cenários Éticos 💡", cor="blue")
        self.ui.escrever("Responda aos cinco dilemas com as alternativas (a, b ou c):\n")
        self.ui.pausar()
        selecionadas = random.sample(self.perguntas, k=5)
        
        # Looping de perguntas
        for i, pergunta in enumerate(selecionadas, 1): 
            Utils.limparTela()
            
            # Usando Panel para exibir o cenário
            pergunta_texto = Text(pergunta['pergunta'], justify="left")
            panel_content = [pergunta_texto, ""]
            for letra, alternativa in pergunta["alternativas"].items():
                panel_content.append(Text(f"({letra}) {alternativa}"))

            self.ui.console.print(Panel(
                Text("\n".join(str(c) for c in panel_content)),
                title=f"Cenário {i}",
                border_style="blue",
                expand=False
            ))
            
            self.ui.console.print(Rule(style="blue"))

            while True:
                resposta = Utils.naoVazio("Digite ('a','b','c') ou 'sair' para encerrar: ").lower()
                match resposta:
                    case 'a'| 'b'|'c':
                        break
                    case 'sair': 
                        self.ui.escrever("Ok. Vamos encerrar por aqui...")
                        self.ui.pausar()
                        self.users.salvarUsuarios()
                        return pontuacao
                    case _:
                        self.ui.console.print("[red]Opção inválida![/red]\n ") 
            
            pontos_resposta = pergunta.get("pontuacoes", {}).get(resposta, 0)
            pontuacao += pontos_resposta
            
            self.ui.console.print(f"\n[green]✅ Você ganhou {pontos_resposta} ponto(s) nesta pergunta.[/green]")
            self.ui.escrever(pergunta["comentario"][resposta], style="italic")
            self.ui.pausar()

            texto_resposta = pergunta['alternativas'][resposta]
            data_resposta = time.strftime("%d/%m/%Y")
            registro = {
                'data': data_resposta,               
                'pergunta': pergunta['pergunta'],    
                'resposta_key': resposta,            
                'texto_resposta': texto_resposta,    
                'pontos': pontos_resposta
            }
            user.historico_respostas.append(registro)

        self.users.salvarUsuarios()
        self.ui.console.print(f"\n[bold green]Você concluiu os cenários e ganhou um total de {pontuacao} ponto(s)![/bold green]\n")
        self.ui.pausar()
        return pontuacao
    