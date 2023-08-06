from typing import List

import requests
from bs4 import BeautifulSoup as bs
from pydantic import BaseModel


class Resultado(BaseModel):
    concurso: str = None
    data: str = None
    numeros_sorteados: List = []
    resultado_premio_principal: str = None
    resultados: List = []
    estimativa_prox_sorteio: str = None
    link: str = None


class Loteria:
    def __init__(self) -> None:
        self.url = "https://noticias.uol.com.br/loterias/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.lista_jogos = [
            "mega-sena",
            "quina",
            "lotofacil",
            "lotomania",
            "dupla-sena",
            "timemania",
            "dia-de-sorte",
            "loteca",
            "loteria-federal",
            "lotogol",
        ]

    def todos(self):
        """
        Retorna os resultados de todos os jogos aqui disponiveis.
        """
        resultados = []
        for jogo in self.lista_jogos:
            resultados.append(self.resultado(jogo))
        return resultados

    def resultado(self, jogo: str) -> Resultado:
        """
        Retorna todas as informações do jogo como: concurso, resultado e premiação do jogo.

        Parameters:
            jogo: Nome do jogo que será utilizado para coleta das informações

        Returns:
            Um objeto com todas as informações do jogo.

        """
        page = requests.get(self.url.format(jogo), headers=self.headers)
        soup = bs(page.text, "html.parser")

        concurso = soup.find_all("div", class_="lottery-info")
        info = concurso[0].text.split("|")
        valor_prox_concurso = soup.find("div", class_="alignCenterValor")
        tabela = soup.find("table", class_="data-table")
        resultados = tabela.find("tbody")
        heads = tabela.find("thead")
        chaves = [str(item.text).strip() for item in heads.findAll("td")]

        premiacao = []

        for row in resultados.find_all("tr"):
            premio = {}
            itens = row.find_all("td")
            premio[chaves[0]] = itens[0].text
            premio[chaves[1]] = itens[1].text
            premio[chaves[2]] = itens[2].text

            premiacao.append(premio)

        match jogo:
            case "loteca":
                numeros = []
                placares = soup.find_all("div", class_="lottery-loteca")[0].find_all("div", class_="linecard")
                for i, p in enumerate(placares, start=1):
                    jogos = {}
                    jogos[f"jogo_{i}"] = p.text
                    numeros.append(jogos)

                vencedor_principal = soup.find("div", class_="winners").text
            case "loteria-federal":
                numeros = []
                vencedor_principal = ""
            case _:
                numeros = [s.text for s in soup.find_all("div", class_="lt-result")[0].find_all("div")]
                vencedor_principal = soup.find("div", class_="winners").text

        return Resultado(
            concurso=str(info[0]).strip(),
            data=str(info[1]).strip(),
            numeros_sorteados=numeros,
            resultado_premio_principal=vencedor_principal,
            resultados=premiacao,
            estimativa_prox_sorteio=valor_prox_concurso.text,
            link=self.url.format(jogo),
        )

    def megasena(self):
        return self.resultado("mega-sena")

    def quina(self):
        return self.resultado("quina")

    def lotofacil(self):
        return self.resultado("lotofacil")

    def lotomania(self):
        return self.resultado("lotomania")

    def duplasena(self):
        return self.resultado("dupla-sena")

    def timemania(self):
        return self.resultado("timemania")

    def diadesorte(self):
        return self.resultado("dia-de-sorte")

    def loteca(self):
        return self.resultado("loteca")

    def lotogol(self):
        return self.resultado("lotogol")

    def loteriafederal(self):
        return self.resultado("loteria-federal")
