# PDF MAX


## Before you start you neeed

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Python 3.10.12](https://www.python.org/downloads/release/python-3913/)
* pip install --upgrade pip

Later you will need:
* [NodeJS 20.9.0+npm](https://nodejs.org/en/)

## Add ssh-keys for you profile
You need add keys [here](https://gitlab.com/-/profile/keys) [instruction how to generate](https://coderlessons.com/tutorials/devops/vyuchit-gitlab/gitlab-nastroika-kliucha-ssh)

## Install venv
`cd app` <br />
`python3.10 -m venv venv` <br />
`source ./venv/bin/activate`

## Verfify python version

`python --version` <br />
`Python 3.10.12`

Main thing is monga and provisioning

## Install poetry
`pip install poetry`

## Install poetry dependencies
`cd backend\app` <br />
`poetry install`

## Run application
`python main.py`
