# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_spinproject',
 'django_spinproject.bin',
 'django_spinproject.generic',
 'django_spinproject.modules',
 'django_spinproject.modules.docker_scripts_data',
 'django_spinproject.modules.dockerfile_data',
 'django_spinproject.modules.dockerignore_data',
 'django_spinproject.modules.gitignore_data',
 'django_spinproject.modules.gitlab_ci_data',
 'django_spinproject.modules.pg_readonly_data',
 'django_spinproject.modules.pytest_data',
 'django_spinproject.modules.settings_data',
 'django_spinproject.modules.srta_data',
 'django_spinproject.project_manager']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['django-spinproject = '
                     'django_spinproject.bin.spinproject:main']}

setup_kwargs = {
    'name': 'django-spinproject',
    'version': '2.5.0',
    'description': 'Opinionated version of `startproject` with some popular third-party packages. Starter pack includes: whitenoise, django-environ, logging, GitHub Scripts to Rule Them All, basic Dockerfile and Makefile.',
    'long_description': "# django-spinproject\n\nOpinionated version of `django-admin startproject` that intends to go further and do things that startproject can't do but most people will do anyway. Here's what you get:\n\n* ⚛️ **Whitenoise**: usually you don't need that during local development but one day you're going to deploy your project and find out that it ignores the `static/` folder when running under gunicorn — which is sorta fine because big applications usually serve static files separately via nginx. Smaller apps with small number of assets, however, usually serve them within the same process, which is what whitenoise is for.\n* 🔧 **settings.py**: it's slightly modified to also understand environment variables and `.env` files. This functionality requires the `django-environ` package. Also, app logger is mostly pre-configured for you.\n* 🔒 **Support for marking PostgreSQL databases as read-only**.\n* 🧰 `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [poetry](https://python-poetry.org/), but you can easily adapt them for any Python package manager.\n* 🏗️ **Dockerfile and .dockerignore**: one day your app will go to production, and we've got you covered.\n* 🏛️ **Gitlab CI config**: CI is a good thing.\n* ⚕️ **Pre-configured linter** so you can find some common problems automagically.\n* 🏃 **Pre-configured pytest** because you are going to need unit tests one day.\n* 🗃️ **Auto-checks if you forgot to create migrations** whenever you run tests or CI.\n* *️⃣ **.gitignore**: well, you know why.\n\n## Requirements\n\n* \\*nix system;\n* `django-admin` installed and available from `$PATH`.\n\nGenerated files will work fine in Django >= 2.0, not tested in earlier versions.\n\n## How to use\n\n* Install the package: `pip install django-spinproject`\n* Create a new project: `django-spinproject --create <path>`\n* OR initialize spinproject in your existing project's folder: `django-spinproject --init`\n\nYou're all set. Now you can take a look at the list of available modules: `django-spinproject --help`\n\nUse `django-spinproject --enable` to enable a module, `django-spinproject --upgrade` to apply changes.\n\n## Other commands\n\n* `--create PATH`: create django project in specified path \n* `--init`: create spinproject.json file\n* `--enable MODULE_TO_ENABLE [MODULE_TO_ENABLE ...]`: enable specified module(s). use 'all' to enable all modules\n* `--disable MODULE_TO_DISABLE`: disable specified module\n* `--upgrade [MODULE_TO_UPGRADE [MODULE_TO_UPGRADE ...]]`: upgrade (specified or all) enabled modules\n\n## Available modules\n\n* `gitignore` — Creates `.gitignore` file suitable for most Django projects.\n* `srta` — Creates [Scripts to Rule Them All](https://github.blog/2015-06-30-scripts-to-rule-them-all/) (simplifies life a lot, you should check it out).\n* `pytest` — Creates `pytest.ini` and `.coveragerc` files.\n* `dockerfile` — Creates a Dockerfile.\n* `dockerignore` — Creates `.dockerignore` (you should totally do that).\n* `docker-scripts` — Creates additional SRTA scripts for building and pushing your Docker image.\n* `gitlab-ci` — Creates GitLab CI config, `.gitlab-ci.yml`.\n* `pg-readonly` — Creates a DatabaseWrapper class for readonly connection to PostgreSQL.\n* `settings` — Improves the default `settings.py`, adding support for envvars and `.env` files. Also enables Whitenoise and CLI logger.\n\n## Planned features\n\n(for requests, create an issue or drop me a line at m1kc@yandex.ru)\n\n* login page template (see `experimental` branch)\n\n## Changelog\n\nSee the [Releases](https://github.com/m1kc/django-spinproject/releases) page.\n",
    'author': 'm1kc (Max Musatov)',
    'author_email': 'm1kc@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/m1kc/django-spinproject',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
