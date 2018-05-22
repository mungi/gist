#!/bin/bash
yum -y install epel-release

# Disable firewall and SELinux
systemctl disable firewalld
systemctl stop firewalld
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0

yum -y install git gettext ansible docker nodejs npm gcc-c++ bzip2
yum -y install python-docker-py

systemctl start docker
systemctl enable docker

cd ~
git clone https://github.com/ansible/awx.git
cd awx/installer/
ansible-playbook -i inventory install.yml

reboot
