# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starfyre', 'starfyre.js']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.29.0,<3.0.0']

setup_kwargs = {
    'name': 'starfyre',
    'version': '0.6.0',
    'description': 'A Python Framework for writing Reactive web Front-Ends',
    'long_description': '\n<img alt="Starfyre Logo" src="https://user-images.githubusercontent.com/29942790/221331176-609e156a-3896-4c1a-9386-7bf595dfb879.png" width="350" />\n\n# Starfyre ⭐🔥\n\n## Introduction:\n\nStarfyre is a library that allows you to build reactive frontends using only Python. It is built using pyodide and wasm, which enables it to run natively in the browser. With Starfyre, you can create interactive, real-time applications with minimal effort. Simply define your frontend as a collection of observables and reactive functions, and let Starfyre handle the rest.\n\nPlease note that Starfyre is still very naive and may be buggy, as it was developed in just five days. However, it is under active development and we welcome contributions to improve it. Whether you are a seasoned web developer or new to frontend development, we hope that you will find Starfyre to be a useful tool. Its intuitive API and simple, declarative style make it easy to get started, and its powerful features allow you to build sophisticated applications.\n\n\n## Installation:\n\nThe easiest way to get started is to clone `create-starfyre-app` repo. Hosted at [create-starfyre-app](https://github.com/sansyrox/create-starfyre-app)\n\n## Sample Usage\n\n\nsrc/__init__.py\n```python\nfrom starfyre import create_component, render\n\nfrom .component import Component\n\n\ndef main():\n    component = Component()\n    render(create_component(<component></component>))\n```\n\nsrc/component.py\n```python\n\nfrom starfyre import create_component, create_signal\n\n[get_component_state, set_state] = create_signal(0)\n\n\ndef updateCounter(component, *args):\n    set_state(get_component_state(component) + 1)\n\n\ndef Component():\n    return create_component("""<div onClick={updateCounter}>\n        This is the component state\n        <button>Click Here to increment</button> {get_component_state}\n        </div>""",\n    )\n\n```\n\n## Developing Locally\n\n1. `make in-dev`\n\nFor more flexibility, see `make help`\n\n## Feedback\n\nFeel free to open an issue and let me know what you think of it. \n',
    'author': 'Sanskar Jethi',
    'author_email': 'sansyrox@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
