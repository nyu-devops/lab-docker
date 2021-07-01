# lab-docker

[![Build Status](https://travis-ci.com/nyu-devops/lab-docker.svg?branch=master)](https://travis-ci.com/nyu-devops/lab-docker)

What is Docker? How can Docker containers help you build and deploy a cloud native solution as micro-services? This lab will teach you what-you-need-to-know to get started building and running Docker Containers. It covers what Docker is, and more importantly, what Docker is not! You will learn how to deploy and run existing Docker community images, how to create your own Docker images, and how to connect containers together using Docker Compose. If you want to know what all this fuss about containers is about, come to this lab and spin up a few containers and see for yourself why everyone is adopting Docker.

This lab is an example of how to create a Python / Flask / Redis app using Docker on Bluemix

## Setting up your Development Environment

We use Vagrant, VirtualBox, and Docker for virtualizing our development environment. Vagrant is technology that allows you to quickly provision and configure Linux virtual machines on your computer. VirtualBox is a hypervisor like VMware Fusion orr Parallels Desktop that hosts virtual machines. Docker is technology that will run multiple containers within a single Linux host machine. Together they make a powerful development environment that mimics multiple servers in a production environment.

If you are using 2020 or later Mac with an Apple M1 Silicon processor you cannot use VirtualBox because it only runs on Intel base computers and Apple Silicon is ARM based. You should install Docker Desktop instead.

### Intel x86 based install

To get started on Intel, download VirtualBox and Vagrant if you don't have them already:

- Download [VirtualBox](https://www.virtualbox.org) - Used to host virtual machines locally on your workstation

- Download [Vagrant](https://www.vagrantup.com) - Used to auto-provision VMs containing your complete dev environment

Install VirtualBox and then Vagrant. 

```sh
git clone https://github.com/nyu-devops/lab-docker.git
cd lab-docker
vagrant up
vagrant ssh
```

### Apple M1 Silicon install

To get started on Apple M1 Silicon, download Docker Desktop and Vagrant instead of VirtualBox if you don't have them already:

- Download [Docker Desktop](https://www.docker.com/products/docker-desktop) - Used to host containers locally on your workstation that behave like virtual machines.

Vagrant will install Docker into the virtual machine so you don't have to.

```sh
git clone https://github.com/nyu-devops/lab-docker.git
cd lab-docker
vagrant up --provider=docker
vagrant ssh
```

Note the difference between starting vagrant with DOcker is to add `--provider=docker` to the `vagrant up` command.
