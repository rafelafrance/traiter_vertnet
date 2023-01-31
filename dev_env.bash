#!/usr/bin/env bash

if [[ ! -z "$VIRTUAL_ENV" ]]; then
  echo "'deactivate' before running this script."
  exit 1
fi

rm -rf .venv
virtualenv -p python3.11 .venv

source ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

python -m spacy download en_core_web_sm

pip install -e ../traiter

# Used for dev
pip install -U pynvim
pip install -U 'python-lsp-server[all]'
pip install -U autopep8 isort pylint yapf pydocstyle
pip install -U jupyter jupyter_nbextensions_configurator ipyparallel
