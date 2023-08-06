.. _changelog:

=========
Changelog
=========

Versions follow `Semantic Versioning <https://semver.org>`_ (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions with advance notice in the
**Deprecations** section of releases.

.. towncrier-draft-entries::

.. towncrier release notes start


Requirements parsed from 'requirements/base.txt': 'salt>=3005', 'pydantic>=1.8.2', 'aiorun', 'importlib-metadata>=3.4.0,<5.0.0; python_version < "3.8"', 'drain3', 'psutil', 'backoff'
Requirements parsed from 'requirements/tests.txt': 'pytest>=6.0.0', 'pytest-salt-factories==0.911.0', 'pytest-asyncio'
Requirements parsed from 'requirements/dev.txt': 'nox', 'pre-commit', 'mypy>=0.910', 'types-attrs', 'types-setuptools', 'pylint==2.12.2', 'astroid==2.9.3', 'pylint-pydantic', 'pyenchant', 'flake8', 'flake8-mypy-fork', 'flake8-docstrings', 'flake8-typing-imports'
Requirements parsed from 'requirements/tests.txt': 'pytest>=6.0.0', 'pytest-salt-factories==0.911.0', 'pytest-asyncio'
Requirements parsed from 'requirements/docs.txt': 'furo', 'sphinx', 'sphinx-copybutton', 'sphinx-prompt', 'sphinxcontrib-spelling', 'sphinxcontrib-towncrier >= 0.2.1a0', 'autodoc_pydantic'
Requirements parsed from 'requirements/docs-auto.txt': 'sphinx-autobuild'
Requirements parsed from 'requirements/changelog.txt': 'towncrier==21.9.0rc1'
Requirements parsed from 'requirements/build.txt': 'twine', 'build>=0.7.0'
0.0.1 (2023-04-28)
==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

No significant changes.


1.0.0 (2022-07-05)
==================

Features
--------

- `#22 <https://github.com/saltstack/pytest-skip-markers/issues/22>`_: Pipelines now have access to caching.

  * There's a cache(dictionary) shared among the whole pipeline where each of the ``collect``, ``process`` and ``forward`` executions can store and grab data from.
  * Additionally, each of ``collect``, ``process`` and ``forward`` plugins in a pipeline execution have their own caching, not shared. Could be used to store state between executions.



Trivial/Internal Changes
------------------------

- `#14 <https://github.com/saltstack/pytest-skip-markers/issues/14>`_: Update copyright headers
