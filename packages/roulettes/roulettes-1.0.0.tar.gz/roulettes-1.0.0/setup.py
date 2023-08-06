# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roulettes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'roulettes',
    'version': '1.0.0',
    'description': 'Add roulettes to your something.',
    'long_description': "# Roulettes\nThis little thing builded by Ivulka allows you to build your own roulettes in python! It provides the mechanism to generate random pick between items with chances.\n\n## How to use?\nFirst, you need to use `pip install roulettes` in terminal. Now you can use roulettes.\n\n### Usage\nThis package is very simple but I think it's sufficient. It has only one function with only one argument: `roulette(<content>)` <br><br>\nHow to use it? Okay, first think you need to know it returns the genrated value so you must use it like this: `x = roulette(<content>)` <br><br>\nThe argument is the content of the roulette. You can save it to a variable if you don't want to have a long code. It's structure is this:\n``` python\n[\n  {\n    'item': <item name>,\n    'chance': <chance>\n  },\n  {\n    'item': <item name>,\n    'chance': <chance>\n  } ...\n]\n```\nNote the chance don't must be in a percentage so it's easier to calculate.\n\n### Example\nThis is an example of a code that works:\n``` python\nimport roulettes\n\nsome_roulette = [\n{'item': '100$', 'chance': 1},\n{'item': '50$', 'chance': 2},\n]\n\nmoney = 10000\n\nreward = roulettes.roulette(some_roulette)\nif reward == '100$':\n  money += 100\nelif reward == '50$':\n  money += 50\nprint(f'{money}$')\n```",
    'author': 'Ivulka',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
