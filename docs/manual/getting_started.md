# Getting Started

## Command line usage

```bash
# Print help
$ ./backbacker.py --help
```

## Dependencies & Virtualenv

* `requirements.txt` lists runtime dependencies
* `requirements-dev.txt` lists dependencies for development

It is recommended to install the dependencies and run the tool in a *virtualenv*.
Virtualenv is a tool to create an "isolated" Python environment.
It helps to keep your base system clean and reduces dependency conflicts.

```bash
$ cd <project>
 
# create environment with default python version
$ virtualenv --no-site-packages venv
# create environment with python 3.4 (Linux)
$ virtualenv --no-site-packages -p /usr/bin/python34 venv

# activate virtualenv (Linux)
$ source venv/bin/activate
# activate virtualenv (Windows)
$ .\venv\Scripts\activate

# install development dependencies
$ pip3 install -r requirements-dev.txt
 
# Print help
$ ./backbacker.py --help
 
# deactivate and destroy environment
$ deactivate
$ rm -rf venv/
```

## Development & Build Management

`setup.py` contains extra commands for development:

```bash
$ cd <project>

# print extra commands (Linux)
$ ./setup.py --help-commands
# print extra commands (Windows)
$ python setup.py --help-commands

$ package           BACKBACKER: Create a Python Built Distribution package.
$ check_code        BACKBACKER: Run code analysis with pylint.
$ check_style       BACKBACKER: Run style checkers.
$ check_style_code  BACKBACKER: Run style checker for code with pep8.
$ check_style_doc   BACKBACKER: Run style checker for docstrings with pep257.
$ documentation     BACKBACKER: Create API and manual documentation.
$ coverage          BACKBACKER: Generate unit test coverage report.
```
