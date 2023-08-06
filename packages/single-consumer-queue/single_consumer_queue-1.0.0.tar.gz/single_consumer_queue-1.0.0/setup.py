# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['single_consumer_queue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'single-consumer-queue',
    'version': '1.0.0',
    'description': 'Asyncio high-performance single consumer queue',
    'long_description': "# Single Consumer Queue\nSingle Consumer Queue is a Python library that provides an alternative to the standard asyncio.Queue for single consumer scenarios. It consists of two classes: SingleConsumerQueue and SingleConsumerPriorityQueue. Both classes implement the AbstractSingleConsumerQueue abstract base class, which provides the basic functionality of a single consumer queue.\n\n## Why Single Consumer Queue?\nIn some scenarios, the standard asyncio.Queue can be slower than necessary. This is because asyncio.Queue is designed to be used with multiple consumers, which means that it has additional overhead to handle multiple concurrent accesses. If you only have one consumer, you can use SingleConsumerQueue or SingleConsumerPriorityQueue to reduce this overhead and improve performance.\n\n## How to use Single Consumer Queue\nInstallation\nYou can install Single Consumer Queue using pip:\n\n```pip install single-consumer-queue```\n\n## Usage\nHere's an example of how to use SingleConsumerQueue:\n\n```\nasync def consumer(queue: SingleConsumerQueue | SingleConsumerPriorityQueue):\n    async for item in queue.start_consuming():\n        print(item)\n```\n\nSingleConsumerQueue raises exception if you try to add multiple consumers:\n\n```\nasync def consumer(queue: SingleConsumerQueue | SingleConsumerPriorityQueue):\n    async for item in queue.start_consuming():\n        print(item)\n\nqueue = SingleConsumerQueue()\nasyncio.create_task(consumer(queue))\nawait asyncio sleep(0.1)\nawait queue.get()  # raises runtime error\n```\n\nLock is checked and acquired when consumer starts and every time that get is awaited.\n\nGet has considerate overhead because it has to use lock every time, so it is recommended to use `start_consuming` generator when you want to consume items in the loop.\n",
    'author': 'Lukas Krocek',
    'author_email': 'krocek.lukas@email.cz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
