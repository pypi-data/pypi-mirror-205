# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfu_torch_lib', 'sfu_torch_lib.modules']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1,<2',
 'mlflow-skinny>=2,<3',
 'numpy>=1,<2',
 'pytorch-lightning>=1.7,<2.0',
 'requests>=2,<3',
 's3fs>=2023,<2024',
 'torch>=1,<2']

setup_kwargs = {
    'name': 'sfu-torch-lib',
    'version': '0.0.38',
    'description': 'Libraries that support the development of machine learning models in PyTorch.',
    'long_description': 'None',
    'author': 'Anderson de Andrade',
    'author_email': 'anderson_de_andrade@sfu.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
