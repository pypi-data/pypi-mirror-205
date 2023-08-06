# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdss', 'mdss.scenarios']

package_data = \
{'': ['*']}

install_requires = \
['MDAnalysis==2.1.0',
 'dictances==1.5.3',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pytest-mock>=3.10.0,<4.0.0',
 'pytest>=7.2.0,<8.0.0',
 'scikit-learn>=1.2.2,<2.0.0']

entry_points = \
{'console_scripts': ['mdss = mdss.run:run',
                     'mdss_scenario_1 = mdss.scenarios.scenario_1:run',
                     'mdss_scenario_2 = mdss.scenarios.scenario_2:run',
                     'mdss_scenario_3 = mdss.scenarios.scenario_3:run']}

setup_kwargs = {
    'name': 'mdsubsampler',
    'version': '0.0.1',
    'description': '',
    'long_description': '# MDSubSampler: Molecular Dynamics SubSampler\n\nMDSubSampler is a Python library and toolkit for a posteriori subsampling of multiple trajectory data for further analysis. This toolkit implements uniform, random, stratified sampling, bootstrapping and targeted sampling to preserve the original distribution of relevant geometrical properties.\n\n## Prerequisites\n\nThis project requires Python (version 3.9.1 or later). To make sure you have the right version available on your machine, try running the following command. \n\n```sh\n$ python --version\nPython 3.9.1\n```\n\n## Table of contents\n\n- [Project Name](#project-name)\n  - [Prerequisites](#prerequisites)\n  - [Table of contents](#table-of-contents)\n  - [Getting Started](#getting-started)\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [Workflow](#workflow)\n    - [Scenarios](#scenarios)\n    - [Parser](#parser)\n    - [Development](#development)\n  - [Authors](#authors)\n  - [License](#license)\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for analysis and development purposes. \n\n## Installation\n\n**BEFORE YOU INSTALL:** please read the [prerequisites](#prerequisites)\n\nTo install and set up the library, run:\n\n```sh\n$ pip install MDSubSampler\n```\n\n## Usage \n\n### Workflow\n\nInput:\n- Molecular Dynamics trajectory \n- Geometric property\n- Atom selection [optional - default is "name CA"]\n- Reference structure [optional] \n- Sample size or range of sizes\n- Dissimilarity measure [optional - default is "Bhattacharyya"]\n\nOutput:\n- .dat file with calculated property for full trajectory (user input)\n- .dat file(s) with calculated property for one or all sample sizes input\n- .xtc file(s) with sample trajectory for one or all sample sizes\n- .npy file(s) with sample trajectory for one or all sample sizes \n- .npy training set for ML purposes for sample trajectory (optional)\n- .npy testing set for ML purposes for sample trajectory (optional)\n- .npy file(s) with sample trajectory for one or for all sample sizes \n- .png file with overlapped property distribution of reference and sample\n- .json file report with important statistics from the analysis\n- .txt log file with essential analysis steps and information\n\n### Scenarios\n\nTo run scenarios 1,2 or 3 you can download your protein trajectory and topology file (.xtc and .gro files) to the data folder and then run the following:\n\n```sh\n$ python mdss/scenarios/scenario_1.py data/<YourTrajectoryFile>.xtc data/<YourTopologyfile>.gro <YourPrefix>\n```\n\n### Parser\n\nIf you are a terminal lover you can use the terminal to run the code and make a choice for the parser arguments. To see all options and choices run:\n\n```sh\n$ python mdss/run.py --help\n```\nOnce you have made a selection of arguments, your command can look like the following example:\n\n```sh\n$ python mdss/run.py \\\n    --traj "data/<YourTrajectoryFile>.xtc" \\\n    --top "data/<YourTopologyFile>.gro" \\\n    --prefix "<YourPrefix>" \\\n    --output-folder "data/<YourResultsFolder>" \\\n    --property=\'DistanceBetweenAtoms\' \\\n    --atom-selection=\'G55,P127\' \\\n    --sampler=\'BootstrappingSampler\' \\\n    --n-iterations=50 \\\n    --size=<SampleSize> \\\n    --dissimilarity=\'Bhattacharyya\'\n```\n\n### Development\n\nStart by either downloading the tarball file from https://github.com/alepandini/MDSubSampler to your local machine or cloning this repo on your local machine:\n\n```sh\n$ git clone git@github.com:alepandini/MDSubSampler.git\n$ cd MDSubSampler\n```\n\nFollowing that, download and install poetry from https://python-poetry.org/docs/#installation\n\n\nFinally, run the following:\n\n```sh\n$ poetry install\n$ poetry build\n$ poetry shell\n```\nYou can now start developing the library.\n\n### Authors\n\n* **Namir Oues** - [namiroues](https://github.com/namiroues)\n* **Alessandro Pandini** [alepandini](https://github.com/alepandini)\n\n### License\n\nThe library is licensed by **GPL-3.0**',
    'author': 'Namir Oues',
    'author_email': 'namir.oues@brunel.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
