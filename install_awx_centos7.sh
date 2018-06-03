#!/usr/bin/env bash
set -x
pip install --upgrade pip
pip uninstall -y urllib3
yum install -y epel-release
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum install -y git2u-core yum-utils device-mapper-persistent-data ansible python-docker-py
pip install urllib3 markupsafe --upgrade

yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-compose

systemctl start docker
systemctl enable docker

cd ~
git clone https://github.com/ansible/awx.git
git clone https://github.com/ansible/awx-logos.git
cd awx/installer/
cp inventory{,.org}
base_dir='/srv/awx'; mkdir -p $base_dir
awxsecret=$(date +%s | sha256sum | base64 | head -c 32 ; echo)
#sed -i 's/^dockerhub_/# dockerhub_/g' inventory
sed -i 's/.*use_container_for_build.*/use_container_for_build=true/g' inventory
sed -i 's/.*awx_official.*/awx_official=true/g' inventory
sed -i 's/.*use_docker_compose.*/use_docker_compose=true/g' inventory
sed -i "s|.*postgres_data_dir.*|postgres_data_dir=${base_dir}/postgress|g" inventory
sed -i "s|.*docker_compose_dir.*|docker_compose_dir=${base_dir}/awx|g" inventory
sed -i "s|.*project_data_dir.*|project_data_dir=${base_dir}/awx/projects|g" inventory
sed -i "s|.*secret_key.*|secret_key=${awxsecret}|g" inventory

ansible-playbook -i inventory install.yml -vv

docker exec awx_task_1 bash -c "pip install softlayer awscli python-nmap"

#yum update -y
