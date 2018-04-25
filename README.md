# lab-docker

[![Build Status](https://travis-ci.org/nyu-devops/lab-docker.svg?branch=master)](https://travis-ci.org/devops/lab-docker)

What is Docker? How can Docker containers help you build and deploy a cloud native solution as micro-services? This lab will teach you what-you-need-to-know to get started building and running Docker Containers in IBM Bluemix. It covers what Docker is, and more importantly, what Docker is not! You will learn how to deploy and run existing Docker community images, how to create your own Docker images and push them to Bluemix, and how to connect containers together using Docker Compose. If you want to know what all this fuss about containers is about, come to this lab and spin up a few containers and see for yourself why everyone is adopting Docker.

This lab is an example of how to create a Python / Flask / Redis app using Docker on Bluemix

## Setting up your Development Environment
You must either install Docker and the Bluemix Cloud Foundry CLI and IBM Container plug-in locally on your computer or use the Vagrant image that is included in this repo. We highly recommend just using Vegrant and VirtualBox.

We use Vagrant, VirtualBox, and Docker for virtualizing our development environment. Vagrant is technology that allows you to quickly provision and configure Linux virtual machines on your computer. VirtualBox is a hypervisor like VMware Fusion that hosts virtual machines. Docker is technology that will run multiple containers within a single Linux host machine. Together they make a powerful development environment that mimics multiple servers in a production environment.

To get started, download VirtualBox and Vagrant if you don't have them already:

Download [VirtualBox](https://www.virtualbox.org) - Used to host virtual machines locally on your workstation

Download [Vagrant](https://www.vagrantup.com) - Used to auto-provision VMs containing your complete dev environment

Install VirtualBox and then Vagrant. If you want to test with `cURL` you will need to have it installed on your laptop if your system doesn't already have it.

VirtualBox will install Docker into the virtual machine so you don't have to.

### Install using Vagrant and VirtualBox

    git clone https://github.com/nyu-devops/lab-docker.git
    cd lab-docker
    vagrant up
    vagrant ssh

#### Note: vagrant up
This `Vagrantfile` requires the `vagrant-docker-compose` plug-in. It will check for it and install it if it is not present. This will cause you to have to invoke `vagrant up` a second time. This is normal behavior.

If you see this when you `vagrant up`
```
Installing the 'vagrant-docker-compose' plugin. This can take a few minutes...
Fetching: vagrant-docker-compose-1.3.0.gem (100%)
Installed the plugin 'vagrant-docker-compose (1.3.0)'!
Dependencies installed, please try the command again.
```

Just issue `vagrant up` again.

### Installing on Mac OS X or Windows
Get Docker Toolbox from the Docker web site and install it:
https://www.docker.com/docker-toolbox

### Installing on Ubuntu Trusty 14.04 (LTS)

    sudo apt-get update
    sudo apt-get install docker-engine

Installing on Other OS See Docker installation guide:
https://docs.docker.com/installation/

### Cloud Foundry Installation for Ubuntu

    wget -O cf-cli-installer_6.24.0_x86-64.deb 'https://cli.run.pivotal.io/stable?release=debian64&version=6.24.0&source=github-rel'
    sudo dpkg -i cf-cli-installer_6.24.0_x86-64.deb
    rm cf-cli-installer_6.24.0_x86-64.deb
    echo Y | cf install-plugin https://static-ice.ng.bluemix.net/ibm-containers-linux_x64

### Enable auto-complete for docker

    $vi /etc/bash.bashrc
    Uncomment the following lines:
    # enable bash completion in interactive shells
    if ! shopt -oq posix; then
      if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
      elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
      fi
    fi
    $source /etc/bash.bashrc

Test it with docker +[tab], you can hit the [tab] after any command
