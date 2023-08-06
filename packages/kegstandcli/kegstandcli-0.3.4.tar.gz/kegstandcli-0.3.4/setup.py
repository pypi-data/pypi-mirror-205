# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kegstandcli',
 'kegstandcli.cli',
 'kegstandcli.infra',
 'kegstandcli.infra.stacks']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk-lib>=2.67.0,<3.0.0',
 'aws-solutions-constructs-aws-apigateway-lambda>=2.36.0,<3.0.0',
 'boto3>=1.17.113,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'constructs>=10.0.0,<11.0.0',
 'copier>=6.2.0,<7.0.0',
 'pyjwt>=2.1.0,<3.0.0',
 'tomlkit>=0.11.7,<0.12.0',
 'xxhash>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['keg = kegstandcli.cli.__main__:kegstandcli']}

setup_kwargs = {
    'name': 'kegstandcli',
    'version': '0.3.4',
    'description': "The Developer's Toolbelt For Accelerating Mean-Time-To-Party on AWS",
    'long_description': '<!-- markdownlint-disable first-line-h1 line-length no-inline-html -->\n<p align="center">\n  <a href="https://kegstand.dev/">\n    <img src="https://kegstand.dev/assets/kegstand-logotype.png" width="540px" alt="Kegstand logo" />\n  </a>\n</p>\n\n<h3 align="center">The Developer\'s Toolbelt For Accelerating <em>Mean Time To Party</em> on AWS</h3>\n<p align="center">Created by <a href="https://jensroland.com/">Jens Roland</a> and fueled by a non-zero amount of alcohol</p>\n<p align="center"><a href="https://kegstand.dev/demo">Watch a 3-minute demo</a></p><!-- markdown-link-check-disable-line -->\n\n<br />\n\n## 🥂💃🕺 Welcome to the Party! 🥂💃🕺\n\nKegstand is a free and open-source framework for creating Python APIs and services. It allows you to rapidly build and deploy services on AWS. We all have better things to do than `print(json.dumps(event))` all day long, and Kegstand is here to help you get to the party &mdash; _and into Prod_ &mdash; a lot faster.\n\n**It provides:**\n\n- A CLI tool for creating and deploying your services.\n- A decorator based API abstracting away the boilerplate of Lambda, API Gateway, Cognito, and more.\n- The full power of CDK to define and deploy arbitrary AWS resources with your services.\n\n> _"Experience a streamlined cloud development process, enhanced productivity, and hit that "party" button sooner with Kegstand!"_ > **&mdash; GPT-4, official spokesbot for the Kegstand team**\n\nLearn more on the [Kegstand website](https://kegstand.dev/).\n\n## Prerequisites\n\n- [Python 3.8+](https://www.python.org/downloads/)\n- [Poetry](https://python-poetry.org/docs/#installation) (recommended)\n- An [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)\n- The [CDK CLI configured on the local machine and initialized on the AWS account](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)\n- The AWS CLI [configured with credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)\n- [Copier](https://copier.readthedocs.io/en/stable/#installation) project scaffolding tool (recommended)\n- [npx](https://docs.npmjs.com/cli/v9/commands/npx) for installing CLI tools (recommended)\n- A well-poured [Belgian style brown ale](https://www.grimbergen.com/)\n\n## Quick start\n\nTo create a service with Kegstand, you\'ll need a Python project with a few dependencies and a folder structure following the Kegstand convention.\n\nYou can create this in a few seconds, either with the Kegstand CLI or using [Copier](https://copier.readthedocs.io/en/stable/#installation).\n\n```shell\n# Using the Kegstand CLI\n> pipx install kegstandcli\n> keg new my-service\n\n# Using Copier\n> copier gh:JensRoland/kegstand-project-template my-service\n```\n\nEither method will create a new project folder called `my-service` containing:\n\n```shell\nmy-service\n├── .gitignore                        # Standard .gitignore file\n├── pyproject.toml                    # Project configuration\n└── src\n    └── api\n        └── hello.py                  # Logic for /hello/\n```\n\nKegstand projects are minimal by design, so a fresh project folder contains just those 3 files. Well, apart from a single, empty `__init__.py` gatecrasher, but we can safely ignore that one.\n\nTo install the dependencies for the new project:\n\n```shell\n> cd my-service\n> poetry install\n```\n\nFinally, to build and deploy the service to AWS:\n\n```shell\n> poetry run keg deploy\n```\n\nYou should now be able to access the API endpoint at `https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello`.\n\n## Documentation\n\nFor further examples and more advanced usage, see the [official documentation](https://github.com/JensRoland/kegstand/blob/main/docs/index.md).\n\n## Roadmap\n\nHere are some notable changes, fixes and features that are planned for development:\n\n## 0.4.0\n\n- [ ] More content on [kegstand.dev](https://kegstand.dev)\n- [ ] Custom domain names\n- [X] Maybe simplify the folder structure from `src/api/resources/<resource-name>/<method>.py` to `src/api/<resource-name>.py`\n\n### Pre-1.0.0\n\n- [ ] Specify event triggers for Lambda functions: S3, SNS, SQS, DynamoDB, Cloudwatch CRON scheduled events, etc.\n- [ ] Pagination helper\n- [ ] [Record a screencast](https://asciinema.org/) for the README\n- [ ] Autogenerated docs using [MkDocs](https://www.mkdocs.org/)\n- [ ] GitHub Actions workflow for pushing docs to the website\n\n### 1.0.0\n\n- [ ] Intuitive and mostly automated API Versioning\n- [ ] Simple way to define/override core API/Lambda properties such as CPU/MEM, Python runtime version, warm pool (!), and concurrency\n- [ ] Deploy Lambda-only microservices with no API Gateway\n\n### Future\n\n- [ ] Configurable log level\n- [ ] Add AWS tags in the Kegstand config and they will be applied to the generated resources\n- [ ] Easily add [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)\n- [ ] Add support for APIs using [FastAPI](https://fastapi.tiangolo.com/) with [Mangum](https://mangum.io/) instead of the default Kegstand API framework, and just provide deployment helpers for the API Gateway and Lambda\n- [ ] Improved output from deploy command; friendly post-deploy instructions for testing your API\n- [ ] Version bumper with [bump2version](https://pypi.org/project/bump2version/)\n- [ ] Include more goodies from [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.11.0/) - tracing, metrics, etc.\n- [ ] Add support for APIs using pure [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.11.0/) instead of the default Kegstand API framework, and just provide deployment helpers for the API Gateway and Lambda\n- [ ] Unit testing helpers (wrap moto and make it all a little more DRY and intuitive)\n- [ ] Secure endpoints which require re-authentication (and/or MFA) so a refreshed token isn’t enough (to, say, delete your account or change your credit card info)\n- [ ] Live Lambda development a la SST\n- [ ] Build and deploy gRPC endpoints (or similar alternative)\n- [ ] Build and deploy GraphQL endpoints\n- [ ] Build and deploy stream processors?\n- [ ] Option to teardown before deploying: `keg deploy --force-redeploy`\n- [ ] Use env vars to populate values in kegstand.toml\n- [ ] Merge Kegstand and Beth into one tool\n- [ ] CDK Pipelines\n- [ ] Support HTTP method-specific files (e.g. `get.py`, `post.py`, etc.)\n- [ ] Upgrade Copier once the [template-deleting bugfix](https://github.com/copier-org/copier/pull/1037) is released\n',
    'author': 'JensRoland',
    'author_email': 'mail@jensroland.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kegstand.dev',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
