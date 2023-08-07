![NewsDash](./readme-assets/poster.jpg)
# NewsDash
[![Python 3.9-3.11](https://img.shields.io/badge/Python-3.9--3.11-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/NaviTheCoderboi/NewsDash.svg)](https://github.com/NaviTheCoderboi/NewsDash)
![GitHub last commit](https://img.shields.io/github/last-commit/NaviTheCoderboi/NewsDash.svg)
![](https://img.shields.io/pypi/v/newsdash?style=flat-square)

***
NewsDash is a fast and reliable Python wrapper for the News API that simplifies accessing the latest news articles from around the world. 📰
***
Made by: NaviTheCoderboi
***

---

!!! note "Note"
    This is a WIP library, please report bugs if you find one

---

## Features

- **Fast performance:** This API wrapper is designed to be fast and efficient, allowing users to retrieve news articles quickly and easily.
- **Reliable functionality:** The wrapper uses best practices to ensure reliable functionality and accuracy in retrieving news articles from the API.
- **Easy-to-use interface:** The API wrapper has an intuitive interface that makes it easy for developers to interact with the API and retrieve news articles without having to worry about the details of the underlying protocol.
- **Built with aiohttp:** The wrapper is built using the popular aiohttp library, which provides high-performance asynchronous HTTP client/server for asyncio and Python. This means the wrapper takes advantage of the latest and greatest in async programming techniques to provide fast and efficient performance.
- **Customizable functionality:** The wrapper has a range of customization options, allowing developers to tailor their use of the API to their specific needs.
- **Flexible data handling:** The wrapper is designed to handle a wide variety of data formats, allowing developers to work with the data in the way that best suits their needs.
- **Well-documented:** The wrapper has clear and comprehensive documentation, making it easy for developers to get up and running quickly and troubleshoot any issues that may arise.
## Installation
```bash
python -m pip install newsdash
```
## Examples
- with client
```python
from newsdash import NewsDash
import asyncio

cl = NewsDash("your_api_key")
async def get_news():
  print(await cl.get_everything(query="tech",pageSize=5))
  print(await cl.get_top_headlines(query="Microsoft"))
  print(await cl.get_sources(country="in",language="en"))

asyncio.run(get_news())
```
- with async context manager
```python
from newsdash import NewsDash
import asyncio

async def main():
  async with NewsDash("api_key") as nd:
    print(await nd.get_everything(query="apple"))

asyncio.run(main())
```
## Important urls
- [NewsApi](https://newsapi.org)
- [NewsDash repository](https://github.com/NaviTheCoderboi/NewsDash)
- [NewsDash pypi](https://pypi.org/project/NewsDash)
- [NewsDash documentation](https://NaviTheCoderboi.github.io/NewsDash)