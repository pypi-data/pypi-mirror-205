# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_voice_assistant']

package_data = \
{'': ['*'], 'python_voice_assistant': ['languages/*']}

install_requires = \
['loguru>=0.7.0,<0.8.0',
 'numpy>=1.24.3,<2.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'silero>=0.4.1,<0.5.0',
 'sounddevice>=0.4.6,<0.5.0',
 'vosk>=0.3.45,<0.4.0']

setup_kwargs = {
    'name': 'python-voice-assistant',
    'version': '0.0.1',
    'description': 'Create your own voice assistant like jarvis',
    'long_description': '# python_voice_assistant\n\n<p align="center">\n      <img src="https://i.ibb.co/MZ3PgBR/python-voice-assistant.png" alt="Project Logo" width="726">\n</p>\n\n<p align="center">\n    <img src="https://img.shields.io/badge/Python-3.10-blueviolet" alt="Python Version">\n    <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Game Version">\n    <img src="https://img.shields.io/badge/License-MIT-success" alt="License">\n</p>\n\n## About\n\nPython package for creating your own voice assistants like Siri or Jarvis\n\n## Installation\n\n```\npip install python_voice_assistant\n```\n\n## Documentation\n\n- [Русский](docs/ru_doc.md)\n- [English](docs/en_doc.md)\n\n## CONTRIBUTORS\n\n- [Zeph1rr](https://github.com/Zeph1rr) (Developer)\n\n## License\n\nProject Python voice assistant is distributed under the MIT license.',
    'author': 'Zeph1rr',
    'author_email': 'grianton535@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
