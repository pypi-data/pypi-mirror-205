<img src="https://bra-loterias.readthedocs.io/en/latest/assets/trevo_icon.png" width="200">

# Bra Loterias
[![Documentation Status](https://readthedocs.org/projects/bra-loterias/badge/?version=latest)](https://notas-musicais.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/JohannPhilipi/bra-loterias/actions/workflows/ci.yaml/badge.svg)](https://github.com/JohannPhilipi/bra-loterias/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/bra-loterias.svg)](https://badge.fury.io/py/bra-loterias)

Bra loterias é um CLI para coletar resultados, conferir e gerar jogos das loterias CAIXA.

## Como instalar o projeto

Para instalação do CLI com PIPX:

```bash
pipx install bra-loterias
```

Ou com PIP:

```bash
pip install bra-loterias
```

## Como usar?

O CLI tem como parâmetro o nome jogo que deseja os resultados. Por exemplo, a mega-sena:

```bash
bra-loterias resultados mega-sena
```

Resultado:

```bash
{
    'concurso': 'concurso 2586',
    'data': 'quarta 26.04.23',
    'numeros_sorteados': ['10', '18', '41', '49', '53', '59'],
    'resultado_premio_principal': 'acumulou',
    'resultados': [
        {'FAIXAS': 'Sena', 'GANHADORES': '0', 'PREMIO (R$)': '0,00'},
        {'FAIXAS': 'Quina', 'GANHADORES': '76', 'PREMIO (R$)': '64.781,77'},
        {'FAIXAS': 'Quadra', 'GANHADORES': '6.010', 'PREMIO (R$)': '1.170,29'}
    ],
    'estimativa_prox_sorteio': 'R$ 50.347.934,06',
    'link': 'https://noticias.uol.com.br/loterias/mega-sena/'
}
```

Para mais opções, você pode consultar tambem a flag `--help`:

```bash
 Usage: bra-loterias resultados [OPTIONS] JOGO

 Retorna o resultado do jogos em questão.

╭─ Arguments ────────────────────────────────────────────────────╮
│ *    jogo      TEXT  Nome do jogo [default: None] [required]   │
╰────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                    │
╰────────────────────────────────────────────────────────────────╯
```
