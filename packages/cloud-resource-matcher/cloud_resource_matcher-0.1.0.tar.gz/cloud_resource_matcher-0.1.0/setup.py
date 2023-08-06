# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_resource_matcher',
 'cloud_resource_matcher.modules',
 'cloud_resource_matcher.modules.base',
 'cloud_resource_matcher.modules.multi_cloud',
 'cloud_resource_matcher.modules.network',
 'cloud_resource_matcher.modules.performance',
 'cloud_resource_matcher.modules.service_limits']

package_data = \
{'': ['*']}

install_requires = \
['optiframe>=0.4.0,<0.5.0', 'pulp>=2.7.0,<3.0.0']

entry_points = \
{'console_scripts': ['bench_base = benches.bench_base:bench',
                     'bench_complete = benches.bench_complete:bench',
                     'bench_mini = benches.bench_mini:bench',
                     'demo = examples.demo:main']}

setup_kwargs = {
    'name': 'cloud-resource-matcher',
    'version': '0.1.0',
    'description': 'A framework to optimize costs of cloud computing deployments.',
    'long_description': '# Cloud Resource Matcher [![PyPI Version](https://img.shields.io/pypi/v/cloud_resource_matcher)](https://pypi.org/project/cloud_resource_matcher/) [![License](https://img.shields.io/github/license/TimJentzsch/cloud_resource_matcher)](./LICENSE)\n\nA framework to optimize cloud computing costs, using [mixed integer programming](https://en.wikipedia.org/wiki/Integer_programming).\n\nThis library should be used together with [`optiframe`](https://github.com/TimJentzsch/optiframe) and [`pulp`](https://github.com/coin-or/pulp).\n`optiframe` is the underlying optimization framework. This library provides modules for cloud computing that you can use with `optiframe`.\n`pulp` is used to implement the mixed integer program. You only need to use it if you want to add additional modules or if you want to configure the solver.\n\n## Prerequisites\n\n- [Python](https://www.python.org/downloads/) >= 3.11\n- [optiframe](https://github.com/TimJentzsch/optiframe)\n\n## Installation\n\n```cli\npip install optiframe\n```\n\n## Usage\n\n### The Modules\n\nThis library provides multiple modules that you can use in `optiframe` for modeling cloud cost optimization problems:\n\n- `base_module`: This module represents the basic decision of which cloud resources should be deployed on which cloud services.\n    It also adds instance demands and flat (upfront) base costs for cloud services.\n    This module must always be added, all other modules depend on it.\n- `performance_module`: A module for performance requirements.\n    It allows you to define performance criteria (such as vCPUs and RAM) and the corresponding demand & supply.\n    Use-based pricing models can also be represented with this module.\n- `network_module`: This module provides the means to encode network connections, maximum latency requirements and network traffic costs.\n- `multi_cloud_module`: If multiple cloud service providers are considered for the decision, this module can be used.\n    It allows you to assign the cloud services to the providers, specify migration cost and enforce a minimum and maximum number of providers to be used.\n- `service_limits_module`: If a cloud service is under very high demand and only a limited number of instances is available for purchase, this module can encode these requirements.\n\n### Code Example\n\nHere is a small example demonstrating how to use this library:\n\n```py\nfrom pulp import LpMinimize\nfrom optiframe import Optimizer, SolutionObjValue\nfrom cloud_resource_matcher.modules.base import BaseData, BaseSolution, base_module\nfrom cloud_resource_matcher.modules.performance import PerformanceData, performance_module\n\n# Specify the data of the problem instance\nbase_data = BaseData(...)\nperformance_data = PerformanceData(...)\n\nsolution = (\n    Optimizer("cloud_cost_optimization", sense=LpMinimize)\n    # Configure which modules you want to use\n    .add_modules(base_module, performance_module)\n    # Add the data of the problem instance\n    .initialize(base_data, performance_data)\n    # Obtain the optimal solution to the problem\n    .solve()\n)\n\n# Extract the total cost of the solution\ncost = solution[SolutionObjValue].objective_value\n# Determine which cloud resource should be matched to which cloud service\nmatching = solution[BaseSolution]\n```\n\nYou can also take a look at the `examples` folder for a more detailed example.\nThe `test/case_studies` folder also contains examples based on the pricing examples from cloud service providers.\n\n### Configuring the Solver\n\nThis library uses `pulp` under the hood and is therefore agnostic to the solver backend that you can use.\nBy default, it uses the CBC solver, which is pre-bundled with `pulp`.\nHowever, it\'s not very fast, so you probably want to change it.\n\nYou can pass any solver object from `pulp` into the `.solve(...)` method.\nTake a look at [this documentation](https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html) for instructions on how to install and configure the solvers.\n\n## Glossary\n\nHere is a small glossary of terms that are used across this project:\n\n- **Cloud resource** (CR): Anything you want to deploy on the cloud, such as virtual machines, serverless functions or databases.\n- **Cloud service** (CS): An offer that you can buy in the cloud, for example Google Cloud C3, Amazon S3 or Azure Functions.\n- **Cloud service provider** (CSP): A company offering cloud services. For example Google Cloud, AWS or Microsoft Azure.\n- **Mixed integer program** (MIP): A mathematical description of optimization problems.\n    Solvers can use this to return an optimal solution to the problem.\n    See also [mixed integer programming](https://en.wikipedia.org/wiki/Integer_programming).\n- **Module**: A component that implements one set of decision criteria for the optimization problem.\n    For example, the network module implements functionality to represent network traffic and latencies.\n    By choosing the modules you want to use, you can configure the functionality of the optimizer.\n    If a decision criteria or pricing model you need to use is not implemented yet, you can define your own modules.\n- **Solver**: A program implementing multiple algorithms to solve mixed integer programs to optimality.\n    Examples include [CBC](https://github.com/coin-or/Cbc) (open source), [SCIP](https://www.scipopt.org/) (open source) and [Gurobi](https://www.gurobi.com/solutions/gurobi-optimizer/) (commercial).\n\n## Development\n\nWe use [Poetry](https://python-poetry.org/docs/#installation) as a package manager, so you have to install it to properly run the project locally.\nThen you can fork and clone the repository and run `poetry install` to install all dependencies.\n\nWe use several tools to ensure a consistent level of code quality:\n\n- Run `poetry run pytest` to run the test suit for the whole project.\n- Run `poetry run mypy .` to check for typing errors.\n- Run `poetry run black .` to format all Python files.\n- Run `poetry run ruff .` to lint all Python files.\n\n## License\n\nThis project is available under the terms of the [MIT license](./LICENSE)\n',
    'author': 'Tim Jentzsch',
    'author_email': 'cloud_resource_matcher.projects@timjen.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TimJentzsch/cloud_resource_matcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
