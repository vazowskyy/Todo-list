#!/bin/bash
apt update -y
apt install -y docker.io docker-compose-plugin git

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu