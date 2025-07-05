import json
import os
import random
import time
from utils import Utils


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
    
    def __init__(self):
        """
        Provê o caminho e a lista de frases.       
        """
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
        
        
    def salvar_frase(self, data, frase):
        """
        Persiste no sistema a frase do dia em JSON, junto com a data.
        Se o diretório ainda não existir, ele é criado automaticamente.
        
        Parâmetros:
            data (str): Data em que a frase foi gerada, no formato "DD/MM/YYYY".
            frase (str): Texto da frase a ser salva no arquivo JSON.
        """
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, 'w', encoding='utf-8') as arq:
            json.dump({"data": data, "frase": frase}, arq, indent=4, ensure_ascii=False)


    def carregar_dados(self) -> dict:
        """ 
        Verificação se já existe uma frase salva para o dia atual
        
        Retorna:
          dict: conteúdo do JSON, ou {} caso o arquivo não exista
                ou esteja corrompido.        
        """
        if os.path.exists(self.caminho):
            try:
                with open(self.caminho, 'r', encoding='utf-8') as arq:
                    return json.load(arq)
            except (json.JSONDecodeError, IOError):
                return {}
        else:
            return {}


    def frase_dia(self):
        """
        Exibe a frase do dia, garantindo que permaneça igual até o dia seguinte.
        Fluxo:
        1- Carrega os dados salvos via 'carregar_dados()'.
        2- Se já há uma frase para hoje, usa-a.
            Caso contrário, escolhe aleatoriamente uma das frases e salva.
        3- Limpa a tela e imprime a frase com borda decorativa.
        """
        hoje = time.strftime("%d/%m/%Y")
        dados = self.carregar_dados()

        if dados.get("data") == hoje:
            frase = dados.get("frase", random.choice(self.frases))
        else:
            frase = random.choice(self.frases)
            self.salvar_frase(hoje, frase)

        borda = "=" * (len(frase) + 4)
        Utils.limpar_tela()
        print("\n✨ Frase do Dia ✨")
        print(borda)
        print(f"| {frase} |")
        print(borda)
