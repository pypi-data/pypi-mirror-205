# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixest']

package_data = \
{'': ['*']}

install_requires = \
['PyHDFE>=0.1.1,<0.2.0',
 'formulaic>=0.3.0,<0.4.0',
 'matplotlib>=3.7,<4.0',
 'numpy>=1.2,<2.0',
 'pandas>=1.5.1,<2.0.0',
 'plotnine>=0.10,<0.11',
 'pytest>=7.2.0,<8.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyfixest',
    'version': '0.3.0',
    'description': 'Draft package for high dimensional fixed effect OLS estimation',
    'long_description': '## PyFixest\n\n<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">\n    <linearGradient id="b" x2="0" y2="100%">\n        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\n        <stop offset="1" stop-opacity=".1"/>\n    </linearGradient>\n    <mask id="a">\n        <rect width="99" height="20" rx="3" fill="#fff"/>\n    </mask>\n    <g mask="url(#a)">\n        <path fill="#555" d="M0 0h63v20H0z"/>\n        <path fill="#a4a61d" d="M63 0h36v20H63z"/>\n        <path fill="url(#b)" d="M0 0h99v20H0z"/>\n    </g>\n    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">\n        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>\n        <text x="31.5" y="14">coverage</text>\n        <text x="80" y="15" fill="#010101" fill-opacity=".3">88%</text>\n        <text x="80" y="14">88%</text>\n    </g>\n</svg>\n\nThis is a draft package (highly experimental!) for a Python clone of the excellent [fixest](https://github.com/lrberge/fixest) package.\n\nFixed effects are projected out via the [PyHDFE](https://github.com/jeffgortmaker/pyhdfe) package.\n\nFor a quick introduction, see the [tutorial](https://s3alfisc.github.io/pyfixest/tutorial/).\n\n```python\nfrom pyfixest import Fixest\nfrom pyfixest.utils import get_data\n\ndata = get_data()\n\nfixest = Fixest(data = data)\nfixest.feols("Y~X1 | X2", vcov = "HC1")\nfixest.summary()\n# ### Fixed-effects: X2\n# Dep. var.: Y\n#\n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.103285    0.172956 -0.597172  0.550393\n```\n\nSupport for more [fixest formula-sugar](https://cran.r-project.org/web/packages/fixest/vignettes/multiple_estimations.html) is work in progress.\n\n',
    'author': 'Alexander Fischer',
    'author_email': 'alexander-fischer1801@t-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
