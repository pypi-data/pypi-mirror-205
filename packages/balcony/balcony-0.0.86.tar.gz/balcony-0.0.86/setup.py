# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balcony', 'balcony.custom_nodes']

package_data = \
{'': ['*'], 'balcony': ['custom_yamls/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.24.80,<2.0.0',
 'inflect>=6.0.0,<7.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'mkdocs-autorefs>=0.4.1,<0.5.0',
 'mkdocs-material>=8.5.7,<10.0.0',
 'mkdocstrings[python]>=0.21.2,<0.22.0',
 'pydantic>=1.10.7,<2.0.0',
 'rich>=13.3.4,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['balcony = balcony.cli:run_app']}

setup_kwargs = {
    'name': 'balcony',
    'version': '0.0.86',
    'description': 'AWS API for humans',
    'long_description': "# balcony - AWS API for humans\n\nbalcony is a read-only CLI tool that simplifies the process of listing all resources on the AWS account.\n\nbalcony dynamically parses AWS SDK(`boto3` library) and analyzes required parameters for each operation. \n\nBy **establishing relations between operations over required parameters**, it's **able to auto-fill** them by reading the related operation beforehand.\n\nBy simply entering their name, balcony enables developers to easily list their AWS resources.\n\n<!-- It uses _read-only_ operations, it does not take any action on the used AWS account. -->\n\n### Installation & Documentation \n\n**[https://oguzhan-yilmaz.github.io/balcony/](https://oguzhan-yilmaz.github.io/balcony/quickstart)**\n\nBalcony's documentation website contains quickstart guide, usage cookbook and more.\n## Features & GIFs\n\n### List available AWS Services \n`balcony aws` to see every AWS service available.\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/aws-services-list.gif)\n\n\n### List Resource Nodes of an AWS Service \n`balcony aws <service-name>` to see every Resource Node of a service.\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/resource-node-list.gif)\n\n\n### Reading a Resource Node \n`balcony aws <service-name> <resource-node>` to read operations of a Resource Node.\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/reading-a-resource-node.gif)\n\n\n### Documentation and Input & Output of Operations\nUse the `--list`, `-l` flag to print the given AWS API Operations documentation, input & output structure. \n \n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/list-option.gif)\n\n\n### Enable Debug messages \nUse the `--debug`, `-d` flag to see what's going on under the hood!\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/debug-messages.gif)\n",
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
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
