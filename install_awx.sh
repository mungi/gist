#!/usr/bin/env bash

sudo yum -y install epel-release 
sudo yum -y install yum-utils ansible git python-pip gcc

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce
sudo systemctl enable docker
sudo systemctl start docker
sudo pip install -U pip docker-compose==1.23.2

git clone https://github.com/ansible/awx.git
cd awx/installer/
mkdir -p /var/awx
sed -i 's/\/tmp\/pgdocker/\/var\/awx\/pgdocker/g' inventory
ansible-playbook -i inventory install.yml -b
