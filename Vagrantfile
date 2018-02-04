# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.synced_folder ".", "/lcp/app"

  config.vm.provision :shell, :path => "deploy_tools/vagrant/setup.sh"

end
