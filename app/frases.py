import json
import os
import random
import time
from .ui import Ui


ARQUIVO_FRASE = os.path.join('dados','frase_dia.json')

class FraseDia:
    """
    Gerencia a persistência e exibição da “Frase do Dia”.

    Responsabilidades:
      - Armazenar a lista de frases possíveis.
      - Carregar a frase já salva para a data atual.
      - Persistir uma nova frase, se ainda não houver para hoje.
      - Exibir a frase do dia no terminal com decoração.
    """
    
    def __init__(self, ui: Ui):
        """
        Inicializa o gerenciador de frases com interface e lista predefinida.

        Args:
            ui (Ui): Interface para exibição da frase no terminal.
        """
        self.ui = ui
        self.caminho = ARQUIVO_FRASE
        self.frases = [
            "A tecnologia é melhor quando une as pessoas em vez de separá-las. - Autor Desconhecido",
            "A verdade pode ser encontrada em um único lugar: o código. - Robert C. Martin",
            "Simplicidade é o último grau de sofisticação. - Leonardo da Vinci",
            "Medir o progresso por linhas de código é como medir a construção de aviões pelo peso. - Bill Gates",
            "A inovação distingue um líder de um seguidor. - Steve Jobs",
            "Primeiro resolva o problema. Depois, escreva o código. - John Johnson",
            "Qualquer tolo escreve código que um computador entende. Bons programadores escrevem código que humanos entendem. - Martin Fowler",
            "Programar é pensar, não digitar. - Autor Desconhecido",
            "Não se preocupe se não funcionar direito. Se tudo desse certo, você estaria sem emprego. - Mosher's Law",
            "Existem 10 tipos de pessoas: as que entendem binário e as que não. - Piada Nerd",
            "A função do bom software é fazer o complexo parecer simples. - Grady Booch",
            "Não documente o problema, corrija-o. - Atli Björgvinsson",
            "Aquele que move montanhas começa carregando pequenas pedras. - Confúcio",
            "O sucesso é a soma de pequenos esforços repetidos dia após dia. - Robert Collier"
        ]
             
    def salvarFrase(self, data, frase):
        """
        Salva a frase do dia no arquivo JSON, criando diretórios se necessário.

        Args:
            data (str): Data da frase no formato "DD/MM/YYYY".
            frase (str): Texto da frase a ser persistida.
        """
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, 'w', encoding='utf-8') as arq:
            json.dump({"data": data, "frase": frase}, arq, indent=4, ensure_ascii=False)

    def carregarDados(self):
        """
        Carrega os dados da frase do dia, se disponíveis.

        Returns:
            dict: Conteúdo do JSON com data e frase,
                ou dicionário vazio em caso de erro ou inexistência.
        """
        if os.path.exists(self.caminho):
            try:
                with open(self.caminho, 'r', encoding='utf-8') as arq:
                    return json.load(arq)
            except (json.JSONDecodeError, IOError):
                return {}
        else:
            return {}

    def fraseDia(self):
        """
        Exibe a frase do dia, persistindo uma nova se ainda não houver para hoje.

        O método verifica se já há uma frase salva para a data atual. Caso contrário,
        escolhe uma aleatória da lista, salva e exibe com formatação no terminal.
        """
        hoje = time.strftime("%d/%m/%Y")
        dados = self.carregarDados()

        if dados.get("data") == hoje:
            frase = dados.get("frase", random.choice(self.frases))
        else:
            frase = random.choice(self.frases)
            self.salvarFrase(hoje, frase)

        borda = "=" * (len(frase) + 4)
        
        self.ui.tituloDaFuncRich("Frase do Dia", cor="magenta")
        
        self.ui.console.print(borda, style="magenta")
        self.ui.escrever(f"| {frase} |", delay=0.02, style="cyan bold")
        self.ui.console.print(borda, style="magenta")