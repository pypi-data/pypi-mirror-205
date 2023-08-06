# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradeexecutor',
 'tradeexecutor.analysis',
 'tradeexecutor.backtest',
 'tradeexecutor.cli',
 'tradeexecutor.cli.commands',
 'tradeexecutor.ethereum',
 'tradeexecutor.ethereum.enzyme',
 'tradeexecutor.ethereum.uniswap_v2',
 'tradeexecutor.ethereum.uniswap_v3',
 'tradeexecutor.monkeypatch',
 'tradeexecutor.state',
 'tradeexecutor.statistics',
 'tradeexecutor.strategy',
 'tradeexecutor.strategy.pandas_trader',
 'tradeexecutor.strategy.qstrader',
 'tradeexecutor.testing',
 'tradeexecutor.utils',
 'tradeexecutor.visual',
 'tradeexecutor.webhook']

package_data = \
{'': ['*'], 'tradeexecutor.ethereum': ['abi/uniswap/*']}

install_requires = \
['ipywidgets>=7.0,<8.0',
 'jupyterlab>=3.5.0,<4.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'pandas-ta>=0.3.14-beta.0,<0.4.0',
 'requests>=2.27.1,<3.0.0',
 'tblib>=1.7.0,<2.0.0',
 'tqdm-loggable==0.1.3',
 'tqdm>=4.64.1,<5.0.0',
 'trading-strategy==0.14']

extras_require = \
{':extra == "data"': ['web3-ethereum-defi==0.18.3'],
 ':extra == "execution"': ['python-logstash-tradingstrategy==0.5.1'],
 'execution': ['typer>=0.4.0,<0.5.0',
               'colorama>=0.4.4,<0.5.0',
               'coloredlogs>=15.0.1,<16.0.0',
               'prompt-toolkit>=3.0.31,<4.0.0',
               'APScheduler>=3.9.1,<4.0.0',
               'python-logging-discord-handler>=0.1.3,<0.2.0',
               'python-dotenv>=0.21.0,<0.22.0',
               'kaleido==0.2.1'],
 'qstrader': ['trading-strategy-qstrader>=0.5,<0.6'],
 'quantstats': ['quantstats>=0.0.59,<0.0.60'],
 'web-server': ['pyramid>=2.0,<3.0',
                'pyramid-openapi3>=0.16.0,<0.17.0',
                'waitress>=2.0.0,<3.0.0',
                'WebTest>=3.0.0,<4.0.0',
                'openapi-core<0.17']}

entry_points = \
{'console_scripts': ['get-latest-release = '
                     'tradeexecutor.cli.latest_release:main',
                     'prepare-docker-env = '
                     'tradeexecutor.cli.prepare_docker_env:main',
                     'trade-executor = tradeexecutor.cli.main:app']}

setup_kwargs = {
    'name': 'trade-executor',
    'version': '0.3',
    'description': 'Algorithmic trading backtesting and execution engine for decentralised finance',
    'long_description': '[![Automated test suite and Docker image build](https://github.com/tradingstrategy-ai/trade-executor/actions/workflows/test-and-build-image.yml/badge.svg)](https://github.com/tradingstrategy-ai/trade-executor/actions/workflows/test-and-build-image.yml)\n\n# Trade Executor: Algorithmic Trading Engine for DeFi \n\n`trade-executor` is a Python framework for backtesting and live execution of algorithmic trading strategies on decentralised exchanges. \n\n**Note**: This is early beta software. [Please pop in to the Discord for any questions](https://tradingstrategy.ai/community). \n\n## Features\n\n- Only trading framework that has been built grounds up for [decentralised finance](https://tradingstrategy.ai/glossary/decentralised-finance)\n- [High quality documentation](https://tradingstrategy.ai/docs/)\n- Support [decentralised markets like Uniswap, PancakeSwap](https://tradingstrategy.ai/docs/overview/supported-markets.html)\n- [Backtesting enginer](https://tradingstrategy.ai/docs/running/backtesting.html)\n- [Live trading](https://tradingstrategy.ai/docs/running/live-trading.html)   \n- [Webhook web server](https://tradingstrategy.ai/docs/running/webhook.html) for JavaScript frontend and monitoring system integration\n- Deploy as [Docker container](https://tradingstrategy.ai/docs/running/cli.html)\n\n## Prerequisites\n\nYou need to know\n\n- Basics of Python \n- Basics of trading\n- [We have collected learning material for developers new to algorithmic trading](https://tradingstrategy.ai/docs/learn/index.html)\n\n## Getting started\n\nFirst study the example code\n\n- [Code examples](https://tradingstrategy.ai/docs/programming/code-examples/running.html)\n- [Trading strategy examples](https://tradingstrategy.ai/docs/programming/code-examples/running.html)\n- [See TradingView PineScript porting example](https://tradingstrategy.ai/blog/avalanche-summit-ii-workshop)\n\n## More information\n\n- [Read documentation on running and backtesting strategies](https://tradingstrategy.ai/docs/running/index.html)\n- Visit [Trading Strategy website to learn about algorithmic trading on decentralised exchanges](https://tradingstrategy.ai)\n- [Join the Discord for any questions](https://tradingstrategy.ai/community)\n\n## Installation\n\n**Note**: The project is under active development. We recommend any developers to use Github master branch\nfor installations.\n\n```shell\ngit clone git@github.com:tradingstrategy-ai/trade-executor.git\ncd trade-executor\ngit submodule update --init --recursive\n\n# Extra dependencies\n# - execution: infrastructure to run live strategies\n# - web-server: support webhook server of live strategy executors\n# - qstrader: still needed to run legacy unit tests\npoetry install -E web-server -E execution -E qstrader -E quantstats\n``` \n\nOr with pip:\n\n```shell\npip install -e ".[web-server,execution,qstrader,quantstats]" \n```\n\n## Architecture overview\n\nHere is an example of a live trading deployment of a `trade-executor` package.\n\n![Architecture overview](docs/deployment-overview.drawio.svg)\n\n## Running tests\n\nSee [internal development documentation](https://tradingstrategy.ai/docs/programming/development.html). \n\n## Community\n\n- [Trading Strategy website](https://tradingstrategy.ai)\n- [Community Discord server](https://tradingstrategy.ai/community#discord)\n- [Blog](https://tradingstrategy.ai/blog)\n- [Twitter](https://twitter.com/TradingProtocol)\n- [Telegram channel](https://t.me/trading_protocol)\n- [Newsletter](https://tradingstrategy.ai/newsletter)\n\n## License \n\n- AGPL\n- [Contact for the commercial dual licensing](https://tradingstrategy.ai/about)\n',
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@tradingstrategy.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tradingstrategy.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
