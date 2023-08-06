# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysats']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.23,<0.30.0', 'numpy>=1.24.1,<2.0.0', 'pyjnius>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'pysats',
    'version': '0.2.2',
    'description': 'GNU Affero General Public License v3',
    'long_description': "# PySATS\n\nThis is a bridge to use some features of [SATS](https://spectrumauctions.org/) in a Python project.\n\n## Requirements\n\n- Python: 3.8+ (required for guaranteeing insertion order in dicts)\n- Pyjnius 1.3.0\n\n## Set up\n\n1. Create a Python environment that satisfied above requirements. To install Pyjnius, follow the steps in <https://pyjnius.readthedocs.io/en/stable/installation.html>#.\n2. Download the latest SATS JAR from <https://github.com/spectrumauctions/sats/releases/>\n3. Place the SATS JAR together with the cplex.jar (which can be found in the CPLEX installation's `bin` folder) together in some directory on your machine, and set the PYJNIUS_CLASSPATH environment variable to the absolute path of this directory.\n\n## Usage\n\nAfter having set up the environment according the the previous section, install the package\n\n```bash\n$ pip install pysats\n...\n```\n\nUse it in your project as follows. Have a look at the `test/` directory for more examples.\n\n```python\nfrom pysats import PySats\n\ngsvm = PySats.getInstance().create_gsvm()\nfor bidder_id in gsvm.get_bidder_ids():\n    goods_of_interest = gsvm.get_goods_of_interest(bidder_id)\n    print(f'Bidder_{bidder_id}: {goods_of_interest}')\n```\n\n## Verify installation\n\nThe best way to verify installation, and check if everything is wired up correctly, is to check out the project and to run the tests:\n\n```bash\n$ python -m unittest\n...\n```\n\n### Alternative to set up locally: Poetry\n\nYou can use Poetry to set up and test pysats locally. Install it as described in <https://python-poetry.org/docs/#installation>, and then run:\n\n```bash\n$ poetry install\n...\n```\n\nThis will install all dependencies automatically. To test the setup, run:\n\n```bash\n$ poetry run python -m unittest\n...\n```\n",
    'author': 'Fabio Isler',
    'author_email': 'islerfab@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marketdesignresearch/pysats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
