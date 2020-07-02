# fintopics

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.com/Ark-Paradigm/fintopics.svg?branch=master)](https://travis-ci.com/Ark-Paradigm/fintopics)
[![Coverage](https://coveralls.io/repos/github/Ark-Paradigm/fintopics/badge.svg?branch=master)](https://coveralls.io/github/Ark-Paradigm/fintopics?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/fintopics.svg)](https://pypi.org/project/fintopics/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Deep Learning for Financial Topic Modeling


## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)
- Add yours!


## Installation
We use [poetry](https://python-poetry.org/) for dependency management. Install it from [here](https://github.com/python-poetry/poetry#installation).
Then install the dependencies using.


```bash
poetry install fintopics
```


## Usage

You can access the help by using the command

```bash
fintopics --help
```

You can prepare the dataset using the following commands:

```bash
# To prepare text data using 100 financial documents
fintopics prepare text --file_limit=100 

# To prepare matrix data using 100 financial documents
fintopics prepare scamat --file_limit=100 
```
The settings can be configured in fintopics.toml file.

## License

[MIT](https://github.com/Ark-Paradigm/fintopics/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [0933a30fc0dc01d374f8c55d7b1e2070b4118d7e](https://github.com/wemake-services/wemake-python-package/tree/0933a30fc0dc01d374f8c55d7b1e2070b4118d7e). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/0933a30fc0dc01d374f8c55d7b1e2070b4118d7e...master) since then.
