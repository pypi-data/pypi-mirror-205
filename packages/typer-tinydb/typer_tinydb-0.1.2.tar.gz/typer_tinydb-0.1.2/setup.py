# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_tinydb', 'typer_tinydb.tests']

package_data = \
{'': ['*'], 'typer_tinydb': ['static/*']}

install_requires = \
['tinydb>=4.7.1,<5.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tcfg = typer_tinydb.typerdb:cfg',
                     'typer-tinydb-config = typer_tinydb.typerdb:config']}

setup_kwargs = {
    'name': 'typer-tinydb',
    'version': '0.1.2',
    'description': 'A Python Typer CLI subcommand boilerplate to manage config files using tinydb',
    'long_description': '\n[![PyPI version](https://badge.fury.io/py/typer-tinydb.svg)](https://badge.fury.io/py/typer-tinydb) [![GitHub License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/arnos-stuff/typer-tinydb/master/LICENSE)\n[![codecov](https://codecov.io/gh/arnos-stuff/typer-tinydb/branch/master/graph/badge.svg?token=7MP5WBU8GI)](https://codecov.io/gh/arnos-stuff/typer-tinydb)\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/arnos-stuff/typer-tinydb/tree/master.svg?style=shield "CircleCI Build Status")](https://dl.circleci.com/status-badge/redirect/gh/arnos-stuff/typer-tinydb/tree/master)\n\n# A Typer config file get/set boilerplate\n\n# Using the boilerplate\n\n## Aliases and subcommands\n\nWe recommand the following aliases, which are readily available out of the box.\n\n- `config`\n- `cfg`\n- `c`\n\nThis way, if your app is named `super-app`\n\nAnd is defined in `super_app.py` roughly as follows:\n\n```python\n\nimport typer\n\n# ... some imports\n\napp = typer.Typer(\n    name=\'super-app\',\n    # ... other args\n)\n```\n\nYou just have to add the following below:\n\n```python\nfrom typer_tinydb import cfg, config # those are typer apps\n\napp.add_typer(cfg) # the cfg app\napp.add_typer(config) # the config app\n```\n\nYou can rename them however you like by using\n\n```python\napp.add_typer(cfg, name=\'my-super-config\')\n```\n\n## Using it on the command line\n\nWith the same configuration as above, your new app can now run the commands:\n\n```bash\nsuper-app cfg list # list config key:value pairs\nsuper-app cfg get some-key # get the values linked to the key \'some-key\'\nsuper-app cfg set some-key \'20-hS407zuqYKQ8tPP2r5\' # store some hash or token into your settings file\nsuper-app cfg set some-key \'20-hS407zuqYKQ8tPP2r5\'\n```\n\nYou can obviously use `super-app config get` and others, or any name you attribute to it.\n\n## Using it within python modules\n\nThe CLI key-values are stored in a tinydb instance that is available by just importing the table named `globals`:\n\n```python\nfrom typer_tinydb import db, globals, where\n```\n\nYou can create any table using the database object `db`, please [check out the tinydb docs !](https://tinydb.readthedocs.io/)\n\nTo get the key just use `where` :\n\n```python\nreturns = globals.search(where(\'param\') == param)\n```\n\nTo insert new values or update existing, use the `upsert` function:\n\n```python\nParam = Query()\n\nglobals.upsert({\n    "param": param,\n    "value": value,\n    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),\n    "machine": socket.gethostname(),\n    },\n    Param.param == param\n)\n```\n# Commands\n\nGo check out the [documentation page 🚀](https://arnos-stuff.github.io/typer-tinydb)',
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://arnos-stuff.github.io/typer-tinydb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
