<p align="center">
  <a href="" rel="noopener">
 <img src="https://www.python.org/static/img/python-logo@2x.png" alt="Project logo"></a>
</p>

<h3 align="center">Project REST API</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/devvspaces/django-restframework-template/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/devvspaces/django-restframework-template/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Django Rest Framework project
    <br>
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This is a Django Rest Framework project. It is a template for building REST APIs with Django Rest Framework. It is built with the following features;

- User Authentication with JWT
- User Registration
- User Login
- User Logout
- User Password Reset
- User Password Change
- User Profile Update
- Users List API
- Users Detail API
- API Keys Integration: Using Secret keys and Public keys
- Admin and API key DRF Permissions

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

For installing the project, you will need to have;

- Python installed. Python version supported is `3.9`. The Github actions use 3.9 for running live tests.

- If Must have PostgreSQL installed. You can use WSL2 to do this on Windows 10 and 11.

> Use postgresql only if you are using it as your default database. If you are using sqlite, you can skip this step.

### Installing

A step by step series of examples that tell you how to get a development environment running.

Clone the project

Setup virtual enviroment & install dependencies

Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
mkdir logs
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
mkdir logs
```

Copy the env.example file to .env

```bash
cp env.example .env
```

Run migrations

```bash
python manage.py migrate
```

Run the server

```bash
python manage.py runserver
```

## 🔧 Running the tests <a name = "tests"></a>

Run tests to make sure all is working before you start contributing

```bash
pytest --no-cov
```

### And coding style tests

This must be used to ensure all coding style guidelines are met

```bash
flake8
```

## 🎈 Usage <a name="usage"></a>

To run the API on your local system.

```bash
python manage.py runserver
```

API server will run on `http://localhost:8000/`. Visit [Swagger](http://localhost:8000/admin/api/docs/) to read the Swagger API documentation.

## 🚀 Deployment <a name = "deployment"></a>

The following method describes how to deploy this on a live system.

### Using Ngrok

- Install [Ngrok](https://ngrok.com/docs/getting-started) on your machine.
- Run API server
- Open CMD / CLI, Run `ngrok http 8000`. `8000` is used if that's the port the API server is listening to. Otherwise, use the listening port.
- The rest is history!

### Using Nginx on an Ubuntu Server

#### Coming soon
<!-- A deploy script.sh should be created to automate the deployment on a new server -->
<br>

## Contributing

Use the following steps below to contribute to this project.

1. First checkout to the `dev` branch
2. Create a new branch for your feature
3. Make your changes
4. Commit your changes
5. Push your changes to your branch
6. Create a pull request to the `dev` branch
7. Wait for review and merge

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.djangoproject.com/) - Web Framework
- [Django Rest Framework](https://www.django-rest-framework.org/) - Building Web APIs
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Redis](https://redis.io/) - In-memory data store
- [Python](https://www.python.org/) - Programming Language

## ✍️ Authors <a name = "authors"></a>

- [@devvspaces](https://github.com/devvspaces) - Project Setup & Initial work

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
