# INSTALLED: the simplest package management from the source code

[![Downloads](https://pepy.tech/badge/instld/month)](https://pepy.tech/project/instld)
[![Downloads](https://pepy.tech/badge/instld)](https://pepy.tech/project/instld)
[![codecov](https://codecov.io/gh/pomponchik/installed/branch/main/graph/badge.svg)](https://codecov.io/gh/pomponchik/installed)
[![Test-Package](https://github.com/pomponchik/installed/actions/workflows/coverage.yml/badge.svg)](https://github.com/pomponchik/installed/actions/workflows/coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/instld.svg)](https://pypi.python.org/pypi/instld)
[![PyPI version](https://badge.fury.io/py/instld.svg)](https://badge.fury.io/py/instld)

Thanks to this package, it is very easy to manage the lifecycle of packages directly from the code.

Install [it](https://pypi.org/project/instld/):

```bash
pip install instld
```

And use as in this example:

```python
import installed


with installed('polog'):
  from polog import log, config, file_writer

  config.add_handlers(file_writer())

  log('some message!')
```

This code installs the [polog](https://github.com/pomponchik/polog) package, imports the necessary objects from there and displays a message. At the end of the program, there will be no excess garbage left in the system. This way you can easily try different packages without bothering with their installation and subsequent removal.
