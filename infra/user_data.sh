#!/bin/bash -xe

apt update -y

apt install -y \
  docker.io \
  docker-compose-plugin \
  git

systemctl enable docker
systemctl start docker
systemctl restart docker

usermod -aG docker ubuntu

docker --version
docker compose version