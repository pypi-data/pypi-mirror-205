# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PortableTab']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'marisa-trie>=0.7.8,<0.8.0', 'pycapnp>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['portabletab = PortableTab.__main__:main']}

setup_kwargs = {
    'name': 'portabletab',
    'version': '0.3.2',
    'description': 'Python package for serializing tables in portable format with Capnp.',
    'long_description': "# PortableTab\n\n*PortableTab* is a Python library that allows for serialization of \ntyped tables into a set of files, as well as deserialization of\nspecific rows extracted from the files.\n\n## Features\n\nThe serialized files are independent of OS and CPU architecture, so it can\nbe used to create portable table which is useful when working with large\ndatasets that need to be shared between different systems or environments.\n\nIt also allows fast deserialization of only specified rows without loading\nthe entire table into memory, so it does not take time to load and\ndeserialize the table on the first access, nor consume memory during execution.\n\n- [Capn' Proto](https://capnproto.org/) is used for serialization,\n  making the file format portable.\n- Since *PortableTab* uses mmap for file access, it does not consume\n  much memory even when handling large tables.\n- Indexes on strings are created using\n  [Marisa-trie](https://github.com/pytries/marisa-trie),\n  the output files are also portable and accessible using mmap.\n\n## Limitations\n\nThe tables are serialized into compact files so they cannot be dynamically\nmodified.\n\n- Rows can only be retrieved at their specified position. If you want to\n  access by an attribute such as *id*, you must create an index on that attribute.\n- Updating records in serialized files is possible but very slow.\n- It is not possible to insert rows in the middle of a serialized file. If you\n  want to insert rows in the middle, the only way is to deserialize\n  the entire table and recreate another table.\n\n## How to use\n\nPlease refer to the documentation at\n[PortableTab Document](https://portabletab.readthedocs.io/en/latest/).\n\n## Development status\n\nUnstable alpha version.\n\n## License\n\nThis package is available according to the MIT license.\n\n## Author\n\nTakeshi SAGARA <sagara@info-proto.com>\n",
    'author': 'Takeshi Sagara',
    'author_email': 'sagara@info-proto.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
