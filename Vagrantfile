# -*- mode: ruby -*-
# vi: set ft=ruby :

# WARNING: You will need the following plugin:
# vagrant plugin install vagrant-docker-compose

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
    # Add Python dev environment
    apt-get update
    apt-get install -y git zip tree python-pip python-dev
    apt-get -y autoremove
    pip install --upgrade pip

    echo "\n******************************"
    echo " Installing Bluemix CLI"
    echo "******************************\n"
    wget -q -O - https://clis.ng.bluemix.net/download/bluemix-cli/latest/linux64 | tar xzv
    cd Bluemix_CLI/
    ./install_bluemix_cli
    cd ..
    rm -fr Bluemix_CLI/
    bluemix config --usage-stats-collect false
    # Install container plugins
    sudo -H -u vagrant bash -c "bx plugin install container-registry -r Bluemix"
    sudo -H -u vagrant bash -c "bx plugin install container-service -r Bluemix"
    # Prove they got installed
    sudo -H -u vagrant bash -c "bx plugin show container-registry"
    sudo -H -u vagrant bash -c "bx plugin show container-service"

    # Install Kubernetes kubectl
    echo "\n******************************"
    echo " Installing KubeCTL"
    echo "******************************\n"
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl

    # Make vi look nice
    sudo -H -u vagrant echo "colorscheme desert" > ~/.vimrc
    # Install app dependencies
    echo "\n******************************"
    echo " Installing App Dependencies"
    echo "******************************\n"
    cd /vagrant
    sudo pip install -r requirements.txt
  SHELL

  ######################################################################
  # Add Redis docker container
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Prepare Redis data share
    sudo mkdir -p /var/lib/redis/data
    sudo chown vagrant:vagrant /var/lib/redis/data
  SHELL

  # Add Redis docker container
  config.vm.provision "docker" do |d|
    d.pull_images "alpine:3.7"
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

end
