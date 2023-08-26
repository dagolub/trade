# MongoTech
[![Flake8](https://github.com/K-I-S-S-Software/cryptopayments-back-end-python/actions/workflows/flake8.yml/badge.svg)](https://github.com/K-I-S-S-Software/cryptopayments-back-end-python/actions/workflows/flake8.yml)
[![Black](https://github.com/mongotech/app/actions/workflows/black.yml/badge.svg)](https://github.com/mongotech/app/actions/workflows/black.yml)
[![Bandit](https://github.com/mongotech/app/actions/workflows/bandit.yml/badge.svg)](https://github.com/mongotech/app/actions/workflows/bandit.yml)
[![MyPy](https://github.com/mongotech/app/actions/workflows/mypy.yml/badge.svg)](https://github.com/mongotech/app/actions/workflows/mypy.yml)
![PyTest](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dagolub/730cda43e9bff219b52954a6390b1c24/raw/mongotech.json)


## Before you start you neeed

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Python 3.10](https://www.python.org/downloads/release/python-3913/)
* pip install --upgrade pip

Later you will need:
* [NodeJS 19.9.0+npm](https://nodejs.org/en/)

## Add ssh-keys for you profile
You need add keys [here](https://gitlab.com/-/profile/keys) [instruction how to generate](https://coderlessons.com/tutorials/devops/vyuchit-gitlab/gitlab-nastroika-kliucha-ssh)

## Git clone 
`git clone git@gitlab.com:K-I-S-S-Software/cryptopayments-back-end-python.git`

## Install venv
`cd app` <br />
`python3.10 -m venv venv` <br />
`source ./venv/bin/activate`

## Verfify python version

`python --version` <br />
`Python 3.10.6`

Main thing is monga and provisioning

## Install poetry
`pip install poetry`

## Install poetry dependencies
`cd backend\app\app` <br />
`poetry install`

## Run application
`python main.py`

## For api testing you need postman

[Postman](https://www.postman.com/downloads/)

## Configure first request Get Token

![get token request](https://github.com/MongoTech/app/raw/main/docs/Screenshot_2022-06-13_at_09.58.56.png)
![add tests to save token](https://github.com/MongoTech/app/raw/main/docs/Screenshot_2022-06-13_at_09.59.11.png)

In enviroment you need to define HOST = http://localhost:8001/api/v1 and pickup username and password from .env file

