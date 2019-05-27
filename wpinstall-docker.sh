#!/usr/bin/env bash
# Wordpress install script by mungi

set -x
INIT_ID="CloudZ"
INIT_PASSWORD="CloudZ"

yum install -y epel-release
yum install -y python-pip yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-compose
systemctl start docker
systemctl enable docker

cd ~
mkdir -p wordpress; cd wordpress

cat << EOF > docker-compose.yml
version: '3.3'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: ${INIT_PASSWORD}
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: ${INIT_PASSWORD}

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "80:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: ${INIT_PASSWORD}
       WORDPRESS_DB_NAME: wordpress
volumes:
    db_data: {}
EOF

docker-compose up -d

timeout 300 bash -c 'while [[ "$(curl --insecure -s -o /dev/null -w ''%{http_code}'' http://localhost:80)" != "200" ]]; do sleep 5; done'

MYIP=$(curl -s whatismyip.akamai.com)
curl -s --data "dbname=wordpress&uname=$INIT_ID&pwd=$INIT_PASSWORD&dbhost=localhost&prefix=wp_&submit=Submit" \
http://$MYIP/wp-admin/setup-config.php?step=2
curl -s --data "weblog_title=CloudZ+Wordpress+QuickStart&user_name=$INIT_ID&admin_password=$INIT_PASSWORD& \
admin_password2=$INIT_PASSWORD&admin_email=admin%40example.com&blog_public=1&Submit=Install+WordPress" \
http://$MYIP/wp-admin/install.php?step=2

#끝 : 아래 IP로 접속해서 확인 요망
echo "http://$MYIP   ID: $INIT_ID   PW: $INIT_PASSWORD"
