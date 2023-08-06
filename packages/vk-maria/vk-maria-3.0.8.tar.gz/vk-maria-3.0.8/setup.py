# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vk_maria',
 'vk_maria.dispatcher',
 'vk_maria.dispatcher.filters',
 'vk_maria.dispatcher.fsm',
 'vk_maria.dispatcher.fsm.storage',
 'vk_maria.dispatcher.fsm.storage.file',
 'vk_maria.dispatcher.fsm.storage.memory',
 'vk_maria.longpoll',
 'vk_maria.types',
 'vk_maria.upload']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3', 'pydotdict>=3.3.11', 'requests>=2.20.1']

setup_kwargs = {
    'name': 'vk-maria',
    'version': '3.0.8',
    'description': 'Simple Vk Bot synchronous framework',
    'long_description': ".. vk_maria documentation master file, created by\n   sphinx-quickstart on Mon Apr  4 14:48:43 2022.\n   You can adapt this file completely to your liking, but it should at least\n   contain the root `toctree` directive.\n\nWelcome to vk_maria's documentation!\n====================================\n\n   .. image:: https://img.shields.io/badge/telegram-vk_maria-blue.svg?style=flat-square\n      :target: https://t.me/vk_maria_ru\n      :alt: [Telegram] vk_maria live\n\n   .. image:: https://img.shields.io/pypi/v/vk_maria.svg?style=flat-square\n      :target: https://pypi.python.org/pypi/vk_maria\n      :alt: PyPi Package Version\n\n   .. image:: https://img.shields.io/pypi/dm/vk_maria.svg?style=flat-square\n      :target: https://pypi.python.org/pypi/vk_maria\n      :alt: PyPi Month Downloads\n\n   .. image:: https://pepy.tech/badge/vk-maria\n      :target: https://pepy.tech/project/vk-maria\n      :alt: PyPi Total Downloads\n\n   .. image:: https://img.shields.io/pypi/pyversions/vk_maria.svg?style=flat-square\n      :target: https://pypi.python.org/pypi/vk_maria\n      :alt: Supported python versions\n\n**vk_maria** очень простой фреймворк для создания ботов сообществ `Vk <https://dev.vk.com/reference>`_, написанный на Python 3.8.\n\nОфициальные ресурсы vk_maria\n----------------------------\n- Новости: `@vk_maria <https://t.me/vk_maria_ru>`_\n- Чат комьюнити: `@vk_maria_ru <https://t.me/vk_maria_ru_chat>`_\n- Pip: `vk_maria <https://pypi.org/project/vk-maria/>`_\n- Docs: `ReadTheDocs <https://vk-maria.readthedocs.io/ru/latest/>`_\n- Source: `Github репозиторий <https://github.com/lxstvayne/vk_maria>`_\n- Issues/Bug tracker: `Github issues tracker <https://github.com/lxstvayne/vk_maria/issues>`_\n\nСильные стороны\n----------------\n- Простота и удобство\n- Наличие конечных автоматов (FSM)\n- Типизированная\n",
    'author': 'lxstvayne',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
