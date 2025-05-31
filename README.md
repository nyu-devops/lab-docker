# NYU DevOps Docker Lab

[![Build Status](https://github.com/nyu-devops/lab-docker/actions/workflows/workflow.yaml/badge.svg)](https://github.com/nyu-devops/lab-docker/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-green.svg)](https://www.python.org/)
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nyu-devops/lab-docker)

What is Docker? How can Docker containers help you build and deploy a cloud native solution as micro-services? This lab will teach you what-you-need-to-know to get started building and running Docker Containers. It covers what Docker is, and more importantly, what Docker is not! You will learn how to deploy and run existing Docker community images, how to create your own Docker images, and how to connect containers together using Docker Compose. If you want to know what all this fuss about containers is about, come to this lab and spin up a few containers and see for yourself why everyone is adopting Docker.

This lab is an example of how to create a Python / Flask / Redis app using Docker.

## Prerequisite Software Installation

This lab uses Docker and Visual Studio Code with the Remote Containers extension to provide a consistent repeatable disposable development environment for all of the labs in this course.

You will need the following software installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the Visual Studio Marketplace

All of these can be installed manually by clicking on the links above or you can use a package manager like **Homebrew** on Mac of **Chocolatey** on Windows.

### Install with homebrew

If you are on a Mac you can easily install this software with [Home Brew](http://brew.sh)

```bash
brew install --cask docker
brew install --cask visual-studio-code
```

You must setup Visual Studio Code as a Mac to launch from the command line using [these instructions](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line). Then you can run the code command to install the remote containers extension.

```bash
code --install-extension ms-vscode-remote.remote-containers
```

You are now ready to work in the lab.

### Alternate using Vagrant

Alternately, you can use [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) to create a consistent development environment in a virtual machine (VM).

You can read more about creating these environments in my article: [Creating Reproducible Development Environments](https://johnrofrano.medium.com/creating-reproducible-development-environments-fac8d6471f35)

## Bring up the development environment

To bring up the development environment you should clone this repo, change into the repo directory:

```bash
$ git clone https://github.com/nyu-devops/lab-docker.git
$ cd lab-docker
```

Depending on which development environment you created, pick from the following:

### Start developing with Visual Studio Code and Docker

Open Visual Studio Code using the `code .` command. VS Code will prompt you to reopen in a container and you should say **yes**. This will take a while as it builds the Docker image and creates a container from it to develop in.

```bash
$ code .
```

Note that there is a period `.` after the `code` command. This tells Visual Studio Code to open the editor and load the current folder of files.

Once the environment is loaded you should be placed at a `bash` prompt in the `/app` folder inside of the development container. This folder is mounted to the current working directory of your repository on your computer. This means that any file you edit while inside of the `/app` folder in the container is actually being edited on your computer. You can then commit your changes to `git` from either inside or outside of the container.

## Running the tests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

Run the tests using `pytest`

```shell
$ make test
```

PyTest is configured via the included `pyproject.toml` file to automatically include the flags `--pspec --cov=service --cov-fail-under=95` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

## What's featured in the project?

This project uses Python Flask and Redis to create a RESTful counter service that can keep track of multiple named counters.

```text
service         <- Package for the service
├── common      <- Common error and log handlers
├── models.py   <- Model for Redis based counter
├── routes.py   <- Controller for REST API
└── static      <- Status HTML assets

tests               <- Tests package
├── test_models.py  <- Test cases for the models 
└── test_routes.py  <- Test cases for the routes
```

The development environment uses **Docker-in-Docker** so that you have an isolated Docker environment within your Docker development container.

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
