# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oxionics_qiskit_provider']

package_data = \
{'': ['*']}

install_requires = \
['qiskit-terra>=0.23.1,<0.24.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'oxionics-qiskit-provider',
    'version': '0.1',
    'description': '',
    'long_description': 'OxIonics Qiskit Provider\n========================\n\nA provider and backend for Qiskit, which executes quantum circuits on the\nOxford Ionics ion traps.\n\nUsage\n-----\n\nUnlike with most Qiskit backends, the Oxford Ionics backend doesn\'t require that\nthe circuit has been transpiled before being passed to `OxIonicsBackend.run`.\nThis is because the OxIonics API accepts arbitrary QASM.\n\n\n### Create a backend\n\nAn authentication token is required:\n\n```python\nfrom oxionics_qiskit_provider import OxIonicsProvider\n\nprovider = OxIonicsProvider("my_token")\nbackend = provider.get_backend()\n```\n\n### Run circuits on the backend\n\n```python\nfrom qiskit.circuit.random import random_circuit\n\nqx = random_circuit(1, 3)\n\njob = backend.run(qx)\nresults = job.results()\n```\n',
    'author': 'Oxford Ionics',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
