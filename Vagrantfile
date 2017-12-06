# -*- mode: ruby -*-
# vi: set ft=ruby :

# WARNING: You will need the following plugin:
# vagrant plugin install vagrant-vbguest

unless Vagrant.has_plugin?("vagrant-docker-compose")
  system("vagrant plugin install vagrant-docker-compose")
  puts "Dependencies installed, please try the command again."
  exit
end

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # expose port 8080 in the VM to 8080 on the host
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "192.168.33.10"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  #
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "512"
    vb.cpus = 1
  end

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy the ssh keys into the vm
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  if File.exists?(File.expand_path("~/.ssh/id_rsa.pub"))
    config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
  end

  ######################################################################
  # Setup a Python development environment
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Add Cloud Foundry CLI to apt-get sources
    wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
    echo "deb http://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
    apt-get update
    apt-get install -y git zip tree python-pip python-dev build-essential cf-cli
    apt-get -y autoremove
    pip install --upgrade pip
    # Install Kubernetes kubectl
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
    # Make vi look nice
    sudo -u ubuntu echo "colorscheme desert" > ~/.vimrc
    # Install app dependencies
    cd /vagrant
    sudo pip install -r requirements.txt
  SHELL

  ######################################################################
  # Add Redis docker container
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Prepare Redis data share
    sudo mkdir -p /var/lib/redis/data
    sudo chown ubuntu:ubuntu /var/lib/redis/data
  SHELL

  # Add Redis docker container
  config.vm.provision "docker" do |d|
    d.pull_images "alpine:3.3"
    d.pull_images "redis:alpine"
    d.run "redis:alpine",
      args: "--restart=always -d --name redis -p 6379:6379 -v /var/lib/redis/data:/data"
  end

  # Add Docker compose
  # Note: you need to install the vagrant-docker-compose or this will fail!
  # vagrant plugin install vagrant-docker-compose
  # config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", run: "always"
  # config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"
  config.vm.provision :docker_compose

  # Install Docker Compose after Docker Engine
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo -H pip install docker-compose
    # Install the IBM Container plugin as vagrant
    sudo -H -u ubuntu bash -c "echo Y | cf install-plugin https://static-ice.ng.bluemix.net/ibm-containers-linux_x64"
  SHELL

end
