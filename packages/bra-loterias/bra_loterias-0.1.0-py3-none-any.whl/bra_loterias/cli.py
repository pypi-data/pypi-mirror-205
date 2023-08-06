from rich.console import Console
from typer import Argument, Typer

from .loteria import Loteria

console = Console()
app = Typer()


@app.command(help="Retorna o resultado do jogos em questão.")
def resultados(jogo: str = Argument(..., help="Nome do jogo")):
    loteria = Loteria()

    try:
        nome_jogo = loteria.lista_jogos.index(jogo)
    except Exception:
        raise ValueError(f"Jogo não encontrado. Tente algum da lista a seguir: {loteria.lista_jogos}")

    match loteria.lista_jogos[nome_jogo]:
        case "mega-sena":
            result = loteria.megasena()
        case "quina":
            result = loteria.quina()
        case "dupla-sena":
            result = loteria.duplasena()
        case "lotofacil":
            result = loteria.lotofacil()
        case "lotogol":
            result = loteria.lotogol()
        case "lotomania":
            result = loteria.lotomania()
        case "loteria-federal":
            result = loteria.loteriafederal()
        case "loteca":
            result = loteria.loteca()
        case "dia-de-sorte":
            result = loteria.diadesorte()
        case "timemania":
            result = loteria.timemania()
        case "todos":
            result = loteria.todos()

    console.print(result.dict())


@app.command(help="Retorna os jogos disponíveis para uso.")
def jogos():
    loteria = Loteria()
    console.print(loteria.lista_jogos)
