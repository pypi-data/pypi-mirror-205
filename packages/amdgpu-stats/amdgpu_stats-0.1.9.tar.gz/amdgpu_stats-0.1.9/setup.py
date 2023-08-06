# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amdgpu_stats']

package_data = \
{'': ['*']}

install_requires = \
['humanfriendly>=10.0', 'textual>=0.10']

entry_points = \
{'console_scripts': ['amdgpu-stats = amdgpu_stats.interface:tui']}

setup_kwargs = {
    'name': 'amdgpu-stats',
    'version': '0.1.9',
    'description': 'A simple module/TUI (using Textual) that provides AMD GPU statistics',
    'long_description': '# amdgpu_stats\n\nA simple Python module/TUI _(using [Textual](https://textual.textualize.io/))_ that shows AMD GPU statistics\n\n![Screenshot of main screen](https://raw.githubusercontent.com/joshlay/amdgpu_stats/master/screens/main.png "Main screen")\n\nThe GPU and temperature nodes (`edge`/`junction`/etc.) are discovered automatically.\n\nPlease see [the module section](#module) or [the docs](https://amdgpu-stats.readthedocs.io/en/latest/) for information on usage as an `import` in other tooling\n\nTested _only_ on `RX6000` series cards; APUs and more _may_ be supported. Please file an issue if finding incompatibility!\n\n## Requirements\nOnly `Linux` is supported. Information is _completely_ sourced from interfaces in `sysfs`.\n\nIt _may_ be necessary to update the `amdgpu.ppfeaturemask` parameter to enable metrics.\n\nThis is assumed present for *control* over the elements being monitored. Untested without. \n\nSee [this Arch Wiki entry](https://wiki.archlinux.org/title/AMDGPU#Boot_parameter) for context.\n\n## Installation / Usage\n```\npip install amdgpu-stats\n```\nOnce installed, run `amdgpu-stats` in your terminal of choice\n\n## Module\n\n*Rudimentary* support as a module exists; functions / variables offered can be found in `amdgpu_stats.utils`\n\nDemonstration:\n```\nIn [1]: import amdgpu_stats.utils\n\nIn [2]: amdgpu_stats.utils.AMDGPU_CARDS\nOut[2]: {\'card0\': \'/sys/class/drm/card0/device/hwmon/hwmon9\'}\n\nIn [3]: amdgpu_stats.utils.get_core_stats(\'card0\')\nOut[3]: {\'sclk\': 640000000, \'mclk\': 1000000000, \'voltage\': 0.79, \'util_pct\': 65}\n\nIn [4]: amdgpu_stats.utils.get_clock(\'card0\', \'core\', format_freq=True)\nOut[4]: \'659 MHz\' \n```\nFeature requests [are encouraged](https://github.com/joshlay/amdgpu_stats/issues) :)\n\n## Documentation\n\nFor more information on the module, see:\n - `help(\'amdgpu_stats.utils\')` in your interpreter\n - [ReadTheDocs](https://amdgpu-stats.readthedocs.io/en/latest/)\n - [the module source](https://github.com/joshlay/amdgpu_stats/blob/master/src/amdgpu_stats/utils.py) for more info\n',
    'author': 'Josh Lay',
    'author_email': 'pypi@jlay.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joshlay/amdgpu_stats',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
