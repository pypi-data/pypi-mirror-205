# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhrp']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3', 'pandas>=1.2.0', 'scikit-learn>=0.24.1', 'scipy>=1.6.0']

setup_kwargs = {
    'name': 'pyhrp',
    'version': '0.0.0',
    'description': '...',
    'long_description': '# pyhrp\n\n[![DeepSource](https://deepsource.io/gh/tschm/hrp.svg/?label=active+issues&show_trend=true&token=qjT_aLQgo_1Xbe2Z9ZNdH3Cx)](https://deepsource.io/gh/tschm/hrp/?ref=repository-badge)\n\nA recursive implementation of the Hierarchical Risk Parity (hrp) approach by Marcos Lopez de Prado.\nWe take heavily advantage of the scipy.cluster.hierarchy package. \n\nHere\'s a simple example\n\n```python\nimport pandas as pd\nfrom pyhrp.hrp import dist, linkage, tree, _hrp\n\nprices = pd.read_csv("test/resources/stock_prices.csv", index_col=0, parse_dates=True)\n\nreturns = prices.pct_change().dropna(axis=0, how="all")\ncov, cor = returns.cov(), returns.corr()\nlinks = linkage(dist(cor.values), method=\'ward\')\nnode = tree(links)\n\nrootcluster = _hrp(node, cov)\n\nax = dendrogram(links, orientation="left")\nax.get_figure().savefig("dendrogram.png")\n```\nFor your convenience you can bypass the construction of the covariance and correlation matrix, the links and the node, e.g. the root of the tree (dendrogram).\n```python\nimport pandas as pd\nfrom pyhrp.hrp import hrp\n\nprices = pd.read_csv("test/resources/stock_prices.csv", index_col=0, parse_dates=True)\nroot = hrp(prices=prices)\n```\nYou may expect a weight series here but instead the `hrp` function returns a `Cluster` object. The `Cluster` simplifies all further post-analysis.\n```python\nprint(cluster.weights)\nprint(cluster.variance)\n# You can drill into the graph by going downstream\nprint(cluster.left)\nprint(cluster.right)\n```\n\n## Installation:\n```\npip install pyhpr\n```\n',
    'author': 'Thomas Schmelzer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tschm/pyhrp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)
