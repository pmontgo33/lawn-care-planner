# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  #config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "10.10.10.10"
  config.vm.synced_folder ".", "/home/vagrant/app"

  config.vm.provision :shell, :path => "deploy_tools/vagrant/setup.sh"

end
