# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixest']

package_data = \
{'': ['*']}

install_requires = \
['PyHDFE>=0.1.1,<0.2.0',
 'formulaic>=0.5.0,<0.6.0',
 'numba==0.56.4',
 'numpy>=1.2,<2.0',
 'pandas>=1.5.1,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyfixest',
    'version': '0.2.0',
    'description': 'Draft package for high dimensional fixed effect OLS estimation',
    'long_description': '## pyfixest\n\nThis is a draft package (highly experimental!) for a Python clone of the excellent [fixest](https://github.com/lrberge/fixest) package.\n\nFixed effects are projected out via the [PyHDFE](https://github.com/jeffgortmaker/pyhdfe) package.\n\n```python\nfrom pyfixest.fixest import Fixest\nfrom pyfixest.utils import get_data\n\ndata = get_data()\n\nfixest = Fixest(data = data)\nfixest.feols("Y~X1 | X2", vcov = "HC1")\nfixest.summary()\n# ### Fixed-effects: X2\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.103285    0.172956 -0.597172  0.550393\n\nfixest.feols("Y~X1  | X2 + X3 + X4", vcov = "HC1")\nfixest.summary()\n# ### Fixed-effects: X2\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.103285    0.172956 -0.597172  0.550393\n# ---\n# \n# ### Fixed-effects: X2+X3+X4\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.010369    0.010073 -1.029451  0.303268\n\nfixest.feols("Y~X1 | csw0(X3, X4)", vcov = "HC1")\nfixest.summary()\n# ### Fixed-effects: X2\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.103285    0.172956 -0.597172  0.550393\n# ---\n# \n# ### Fixed-effects: X2+X3+X4\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.010369    0.010073 -1.029451  0.303268\n# ---\n# \n# ### Fixed-effects: 0\n# Dep. var.: Y\n# \n#            Estimate  Std. Error   t value  Pr(>|t|)\n# Intercept  7.386158    0.187825 39.324716  0.000000\n#        X1 -0.163744    0.186494 -0.878008  0.379939\n# ---\n# \n# ### Fixed-effects: X3\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.117885    0.178649 -0.659867  0.509339\n# ---\n# \n# ### Fixed-effects: X3+X4\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.063646    0.074751 -0.851439  0.394525\n# ---\n\n# change inference to HC3\n fixest.vcov("HC3").summary()\n# ### Fixed-effects: X2\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.103285    0.172931 -0.597259  0.550334\n# ---\n# \n# ### Fixed-effects: X2+X3+X4\n# Dep. var.: Y\n# \n#     Estimate  Std. Error  t value  Pr(>|t|)\n# X1 -0.010369    0.010071  -1.0296  0.303198\n# ---\n# \n# ### Fixed-effects: 0\n# Dep. var.: Y\n# \n#            Estimate  Std. Error   t value  Pr(>|t|)\n# Intercept  7.386158    0.187806 39.328639   0.00000\n#        X1 -0.163744    0.186467 -0.878136   0.37987\n# ---\n# \n# ### Fixed-effects: X3\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.117885    0.178623 -0.659961  0.509279\n# ---\n# \n# ### Fixed-effects: X3+X4\n# Dep. var.: Y\n# \n#     Estimate  Std. Error   t value  Pr(>|t|)\n# X1 -0.063646     0.07474 -0.851569  0.394454\n# ---\n\n```\n\nSupport for more [fixest formula-sugar](https://cran.r-project.org/web/packages/fixest/vignettes/multiple_estimations.html) is work in progress.\n\n',
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
