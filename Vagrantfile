# -*- mode: ruby -*-
# vi: set ft=ruby :

######################################################################
# Python 3 / Docker Environment
######################################################################
Vagrant.configure(2) do |config|
  # config.vm.box = "ubuntu/bionic64"
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.hostname = "ubuntu"

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Mac users can comment this next line out but
  # Windows users need to change the permission of files and directories
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=755,fmode=644"]

  ############################################################
  # Configure Vagrant to use VirtualBox on Intel:
  ############################################################
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
    # Fixes some DNS issues on some networks
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  ############################################################
  # Configure Vagrant to use for Docker on Intel or ARM
  ############################################################
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:debian"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true
    docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:ro"]
    # Uncomment to force arm64 for testing images on Intel
    # docker.create_args = ["--platform=linux/arm64"]
  end

  ############################################################
  # Copy some host files to configure VM like the host
  ############################################################

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end
  
  # Copy your .vimrc file so that your VI editor looks right
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  ######################################################################
  # Create a Python 3 development environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Install Python 3 and dev tools 
    apt-get update
    apt-get install -y git vim tree wget jq build-essential python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3
    
    # install docker-compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    
    # Install app dependencies in virtual environment as vagrant user
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install -U pip && pip install wheel'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'

    # Check versions to prove that everything is installed
    python3 --version
  SHELL

  ############################################################
  # Provision Docker with Vagrant before starting kubernetes
  ############################################################
  config.vm.provision "docker" do |d|
    d.pull_images "alpine"
    d.pull_images "python:3.8-slim"
    d.pull_images "redis:6-alpine"
    d.run "redis:6-alpine",
      args: "--restart=always -d --name redis -p 6379:6379 -v redis:/data"
  end

end
