#!/usr/bin/env bash
set -x
timedatectl set-timezone UTC
date > /tmp/checkdate

yum -y install epel-release
yum -y install tcpdump bind-utils mtr iperf3 nmon iftop
yum -y update

# to do something
