# cbmc.py

<!-- Add a badge here -->

[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://pypi.org/project/cbmc.py/)
[![CodeFactor](https://www.codefactor.io/repository/github/itsrqtl/cbmc.py/badge)](https://www.codefactor.io/repository/github/itsrqtl/cbmc.py)
![GitHub issues](https://img.shields.io/github/issues/itsrqtl/cbmc.py)
![GitHub pull requests](https://img.shields.io/github/issues-pr/itsrqtl/cbmc.py)

[![PyPI](https://img.shields.io/pypi/v/cbmc.py)](https://pypi.org/project/cbmc.py/)
[![PyPI - License](https://img.shields.io/pypi/l/cbmc.py)](https://pypi.org/project/cbmc.py/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cbmc.py)](https://pypi.org/project/cbmc.py/)

Unofficial 麥塊匿名發文平台 API Wrapper for Python

## Installation

```sh
pip install cbmc.py
```

## Usage

```py
# Import the library
from cbmc import AsyncCbmc, SyncCbmc

api = SyncCbmc()

# Obtain post with post id, raise cbmc.NotFound if not found
api.get_post(1)

# List recent posts, maximum 300 posts.
api.get_posts()

# Directly call the method also works
# Creating an instance is not required, but it is recommended for future updates.
# (some planned new features will require that)
SyncCbmc.get_post(1)

# Also available in async
async def main():
    await AsyncCbmc.get_post(1)
    await AsyncCbmc.get_posts()
```

## Documentation

* [Documentation](docs/DOCS.md)
* [Changelog](CHANGELOG.md)

## Credits

* 麥塊匿名發文平台 API Documents: [CBMC API Docs](https://api.cbmc.club/docs/)
* Inspired by [HansHans135](https://github.com/hanshans135)'s [cbmc](https://github.com/HansHans135/cbmc) library.

## License

This project is licensed under `MIT License`. See the [LICENSE](LICENSE) for more details.
