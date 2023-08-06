# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baichat_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0']

setup_kwargs = {
    'name': 'baichat-py',
    'version': '0.2.0',
    'description': '',
    'long_description': '# BAIChat API Python\n\n## Installation\n\nYou can install it from PyPi\n\n``` shell\npip install baichat-py\n```\n\n## Usage\n\n### Async\n\n``` python\nimport asyncio\n\nloop = asyncio.get_event_loop() \nhello = loop.run_until_complete(chat.async_ask("Hi"))\n\nprint(hello.text)\n\n# => Hello! How can I assist you today?\n```\n\n### Context manager\n\n``` python\nwith BAIChat() as (loop, chat):\n    hello = chat.ask("Hi")\n\n    print(hello.text)\n\n# => Hello! How can I assist you today?\n```\n\n### Delta\n\n``` python\nwith BAIChat() as (loop, chat):\n    hello = chat.ask("Hi")\n\n    for delta in hello:\n        print(delta.text)\n    \n# => Hello\n# => Hello!\n# => Hello! How\n# => Hello! How may\n# => Hello! How may I\n# => Hello! How may I assist\n# => Hello! How may I assist you\n# => Hello! How may I assist you today\n# => Hello! How may I assist you today?\n```\n\n### Sync\n\n``` python\nchat = BAIChat()\nprint(chat.sync_ask("Hello, how are you?").text)\n\n# => Hello! As an AI language model, I don\'t have feelings, but I\'m functioning properly and ready to assist you. How may I help you today?\n```',
    'author': '0xMRTT',
    'author_email': '0xMRTT@proton.me',
    'maintainer': '0xMRTT',
    'maintainer_email': '0xMRTT@proton.me',
    'url': 'https://github.com/Bavarder/baichat-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
