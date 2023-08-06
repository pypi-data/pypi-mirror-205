# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaud_plugins', 'pyaud_plugins._plugins']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.3.2,<7.0.0',
 'black>=21.12,<24.0',
 'constcheck>=0,<1',
 'coverage>=6.2,<8.0',
 'docformatter==1.4',
 'docsig>=0.34.0',
 'environs>=9.4.0,<10.0.0',
 'flynt>=0.75,<0.79',
 'gitpython>=3.1.30,<4.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.930,<1.3',
 'object-colors>=2.0.1,<3.0.0',
 'pyaud>=5.0.1,<7.0.0',
 'pylint>=2.12.2,<3.0.0',
 'pytest-cov>=3,<5',
 'pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'setuptools>=67.2.0,<68.0.0',
 'sphinx-markdown-builder>=0.5.5,<0.6.0',
 'sphinxcontrib-fulltoc>=1.2.0,<2.0.0',
 'sphinxcontrib-programoutput>=0.17,<0.18',
 'toml-sort>=0.20,<0.24',
 'tomli>=2.0.1,<3.0.0',
 'vulture>=2.3,<3.0']

setup_kwargs = {
    'name': 'pyaud-plugins',
    'version': '0.15.0',
    'description': 'Plugin package for Pyaud',
    'long_description': 'pyaud-plugins\n=============\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/pyaud-plugins\n    :target: https://pypi.org/project/pyaud-plugins/\n    :alt: PyPI\n.. image:: https://github.com/jshwi/pyaud-plugins/actions/workflows/build.yaml/badge.svg\n    :target: https://github.com/jshwi/pyaud-plugins/actions/workflows/build.yaml\n    :alt: Build\n.. image:: https://github.com/jshwi/pyaud-plugins/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/pyaud-plugins/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://results.pre-commit.ci/badge/github/jshwi/pyaud-plugins/master.svg\n   :target: https://results.pre-commit.ci/latest/github/jshwi/pyaud-plugins/master\n   :alt: pre-commit.ci status\n.. image:: https://codecov.io/gh/jshwi/pyaud-plugins/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/pyaud-plugins\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/pyaud-plugins/badge/?version=latest\n    :target: https://pyaud-plugins.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n    :alt: isort\n.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg\n    :target: https://github.com/PyCQA/docformatter\n    :alt: docformatter\n.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen\n    :target: https://github.com/PyCQA/pylint\n    :alt: pylint\n.. image:: https://img.shields.io/badge/security-bandit-yellow.svg\n    :target: https://github.com/PyCQA/bandit\n    :alt: Security Status\n.. image:: https://snyk.io/test/github/jshwi/pyaud-plugins/badge.svg\n    :target: https://snyk.io/test/github/jshwi/pyaud-plugins/badge.svg\n    :alt: Known Vulnerabilities\n.. image:: https://snyk.io/advisor/python/pyaud-plugins/badge.svg\n    :target: https://snyk.io/advisor/python/pyaud-plugins\n    :alt: pyaud-plugins\n\nPlugin package for Pyaud\n------------------------\n\nDependencies\n------------\n\n``pip install pyaud``\n\nInstall\n-------\n\n``pip install pyaud-plugins``\n\nDevelopment\n-----------\n\n``poetry install``\n\nUsage\n-----\n\nSee `pyaud <https://github.com/jshwi/pyaud#pyaud>`_\n\nPlugins\n-------\n\n``pyaud`` will automatically load this package on search for all packages prefixed with `"pyaud_"`\n\nFor writing plugins see `docs <https://jshwi.github.io/pyaud/pyaud.html#pyaud-plugins>`_\n\nThis package contains the following plugins on running `pyaud modules`\n\n.. code-block:: console\n\n    about-tests     -- Check tests README is up-to-date\n    audit           -- Read from [audit] key in config\n    change-logged   -- Check commits with loggable tags are added to CHANGELOG\n    clean           -- Remove all unversioned package files recursively\n    commit-policy   -- Test commit policy is up to date\n    const           -- Check code for repeat use of strings\n    coverage        -- Run package unit-tests with `pytest` and `coverage`\n    docs            -- Compile package documentation with `Sphinx`\n    doctest         -- Run `doctest` on all code examples\n    doctest-package -- Run `doctest` on package\n    doctest-readme  -- Run `doctest` on Python code-blocks in README\n    files           -- Audit project data files\n    format          -- Audit code with `Black`\n    format-docs     -- Format docstrings with `docformatter`\n    format-str      -- Format f-strings with `flynt`\n    generate-rcfile -- Print rcfile to stdout\n    imports         -- Audit imports with `isort`\n    lint            -- Lint code with `pylint`\n    params          -- Check docstring params match function signatures\n    sort-pyproject  -- Sort pyproject.toml file with `toml-sort`\n    test            -- Run all tests\n    tests           -- Run the package unit-tests with `pytest`\n    toc             -- Audit docs/<NAME>.rst toc-file\n    typecheck       -- Typecheck code with `mypy`\n    unused          -- Audit unused code with `vulture`\n    whitelist       -- Check whitelist.py file with `vulture`\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/pyaud-plugins/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
