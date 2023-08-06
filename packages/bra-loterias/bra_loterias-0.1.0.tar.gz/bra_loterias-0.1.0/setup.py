# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bra_loterias']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'rich>=13.3.4,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bra-loterias = bra_loterias.cli:app']}

setup_kwargs = {
    'name': 'bra-loterias',
    'version': '0.1.0',
    'description': 'Bra loterias é um CLI para coletar resultados, conferir e gerar jogos das loterias CAIXA. Projeto com finalidades educacionais',
    'long_description': '<img src="https://bra-loterias.readthedocs.io/en/latest/assets/trevo_icon.png" width="200">\n\n# Bra Loterias\n[![Documentation Status](https://readthedocs.org/projects/bra-loterias/badge/?version=latest)](https://notas-musicais.readthedocs.io/en/latest/?badge=latest)\n[![CI](https://github.com/JohannPhilipi/bra-loterias/actions/workflows/ci.yaml/badge.svg)](https://github.com/JohannPhilipi/bra-loterias/actions/workflows/ci.yaml)\n[![PyPI version](https://badge.fury.io/py/bra-loterias.svg)](https://badge.fury.io/py/bra-loterias)\n\nBra loterias é um CLI para coletar resultados, conferir e gerar jogos das loterias CAIXA.\n\n## Como instalar o projeto\n\nPara instalação do CLI com PIPX:\n\n```bash\npipx install bra-loterias\n```\n\nOu com PIP:\n\n```bash\npip install bra-loterias\n```\n\n## Como usar?\n\nO CLI tem como parâmetro o nome jogo que deseja os resultados. Por exemplo, a mega-sena:\n\n```bash\nbra-loterias resultados mega-sena\n```\n\nResultado:\n\n```bash\n{\n    \'concurso\': \'concurso 2586\',\n    \'data\': \'quarta 26.04.23\',\n    \'numeros_sorteados\': [\'10\', \'18\', \'41\', \'49\', \'53\', \'59\'],\n    \'resultado_premio_principal\': \'acumulou\',\n    \'resultados\': [\n        {\'FAIXAS\': \'Sena\', \'GANHADORES\': \'0\', \'PREMIO (R$)\': \'0,00\'},\n        {\'FAIXAS\': \'Quina\', \'GANHADORES\': \'76\', \'PREMIO (R$)\': \'64.781,77\'},\n        {\'FAIXAS\': \'Quadra\', \'GANHADORES\': \'6.010\', \'PREMIO (R$)\': \'1.170,29\'}\n    ],\n    \'estimativa_prox_sorteio\': \'R$ 50.347.934,06\',\n    \'link\': \'https://noticias.uol.com.br/loterias/mega-sena/\'\n}\n```\n\nPara mais opções, você pode consultar tambem a flag `--help`:\n\n```bash\n Usage: bra-loterias resultados [OPTIONS] JOGO\n\n Retorna o resultado do jogos em questão.\n\n╭─ Arguments ────────────────────────────────────────────────────╮\n│ *    jogo      TEXT  Nome do jogo [default: None] [required]   │\n╰────────────────────────────────────────────────────────────────╯\n╭─ Options ──────────────────────────────────────────────────────╮\n│ --help          Show this message and exit.                    │\n╰────────────────────────────────────────────────────────────────╯\n```\n',
    'author': 'Johann Philipi',
    'author_email': 'joliveira.info@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
