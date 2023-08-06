# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awesome_object_store']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage==1.44.0',
 'minio>=7.1.1,<8.0.0',
 'pandas>=1.4.1,<2.0.0',
 'starlette>=0.16.0']

setup_kwargs = {
    'name': 'awesome-object-store',
    'version': '2.2.1',
    'description': 'minio wrapper to perform task like pandas dataframe upload, download',
    'long_description': '[![Stable Version](https://badge.fury.io/py/awesome-object-store.svg)](https://pypi.org/project/awesome-object-store/)\n[![tests](https://github.com/MoBagel/awesome-object-store/workflows/develop/badge.svg)](https://github.com/MoBagel/awesome-object-store)\n[![Coverage Status](https://coveralls.io/repos/github/MoBagel/awesome-object-store/badge.svg?branch=develop)](https://coveralls.io/github/MoBagel/awesome-object-store?branch=develop)\n\n# Awesome Object Store \n\nA library that extends minio python client to perform more complex task like read/write pandas DataFrame, json file, ...etc\n\n# Feature\n* list_buckets: list all buckets.\n* list_objects: list object under a prefix.\n* put_as_json: put a dict as json file on s3.\n* exists: check if an object exist on s3.\n* remove_dir: remove a directory on s3.\n* upload_df: Upload df as csv to s3.\n* get_json: Get as dict from a json file on s3.\n* get_df: Get a dataframe from a csv object on s3.\n* remove_objects: Remove objects.\n* download: Downloads data of an object to file.\n\n# Development\n## run unit test\n1. getting service account credential:\n   1. visit google cloud console\n   1. go to project 8ndpoint-datalake-dev -> Security -> Secret Manager -> awesome-object-store-unit-test\n   1. action -> view secret value\n   1. store the value in tests/service-account.json\n2. run ./run_test.sh\n',
    'author': 'Schwannden Kuo',
    'author_email': 'schwannden@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MoBagel/awesome-object-store',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
