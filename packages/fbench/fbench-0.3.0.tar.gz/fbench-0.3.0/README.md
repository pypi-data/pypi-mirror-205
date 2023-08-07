<h1 align="center">fBench</h1>

<p align="center">
<a href="https://pypi.org/project/fbench"><img alt="pypi" src="https://img.shields.io/pypi/v/fbench"></a>
<a href="https://readthedocs.org/projects/fbench/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/fbench/badge/?version=latest"></a>
<a href="https://github.com/estripling/fbench/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/fbench/actions/workflows/ci.yml/badge.svg?branch=main"></a>
<a href="https://codecov.io/gh/estripling/fbench"><img alt="coverage" src="https://codecov.io/github/estripling/fbench/coverage.svg?branch=main"></a>
<a href="https://github.com/estripling/fbench/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/fbench"></a>
</p>

## About

A collection of benchmark functions:

- [Documentation](https://fbench.readthedocs.io/en/stable/index.html)
- [Overview of fBench functions](https://fbench.readthedocs.io/en/stable/fBench-functions.html)
- [API Reference](https://fbench.readthedocs.io/en/stable/autoapi/fbench/index.html)

## Installation

`fbench` is available on [PyPI](https://pypi.org/project/fbench/) for Python 3.8+:

```console
pip install fbench
```

## Examples

The [`ackley`](https://fbench.readthedocs.io/en/stable/autoapi/fbench/index.html#fbench.ackley) function:

```python
>>> import fbench
>>> round(fbench.ackley([1, 1]), 4)
3.6254
```

## Contributing to fBench

Your contribution is greatly appreciated!
See the following links to help you get started:

- [Contributing Guide](https://fbench.readthedocs.io/en/latest/contributing.html)
- [Developer Guide](https://fbench.readthedocs.io/en/latest/developers.html)
- [Contributor Code of Conduct](https://fbench.readthedocs.io/en/latest/conduct.html)

## License

`fbench` was created by fBench Developers.
It is licensed under the terms of the BSD 3-Clause license.
