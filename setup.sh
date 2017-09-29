#!/bin/bash

# Create influxdb network
docker network create influxdb

# Get influxdb container
sudo docker pull influxdb:1.3.5-alpine

# Create data dirs
mkdir -p /mnt/fatboy/sauron/influxdb/conf
mkdir -p /mnt/fatboy/sauron/influxdb/data
mkdir -p /mnt/fatboy/sauron/influxdb/wal

# Get config file
cd /mnt/fatboy/sauron/influxdb/conf
docker run --rm influxdb:1.3.5-alpine influxd config > influxdb.conf
cd ~/sauron

# Install systemd service file
sudo cp etc/systemd/influxdb.service /etc/systemd/system/

# Create database
docker run --rm \
      -e INFLUXDB_DB=house -e INFLUXDB_ADMIN_ENABLED=true \
      -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_USER=password \
      -e INFLUXDB_USER=telegraf -e INFLUXDB_USER_PASSWORD=password \
      -v /mnt/fatboy/sauron/influxdb:/var/lib/influxdb influxdb:1.3.5-alpine \
      /init-influxdb.sh

###########

# Get telegraf container
sudo docker pull telegraf:1.4.1-alpine

# Create conf dir
mkdir -p /mnt/fatboy/sauron/telegraf/conf

# Get config file
cd /mnt/fatboy/sauron/telegraf/conf
docker run --rm telegraf:1.4.1-alpine telegraf config > telegraf.conf
cd ~/sauron

# Install systemd service file
sudo cp etc/systemd/telegraf.service /etc/systemd/system/

############

# Get chronograf container
sudo docker pull chronograf:1.3.8.2-alpine

# Create data dir
mkdir -p /mnt/fatboy/sauron/chronograf

# Install systemd service file
sudo cp etc/systemd/chronograf.service /etc/systemd/system/

#############

# Get kapacitor container
sudo docker pull kapacitor:1.3.3-alpine

# Chreate data and conf dirs
mkdir -p /mnt/fatboy/sauron/kapacitor
mkdir -p /mnt/fatboy/sauron/kapacitor/conf

# Get config file
cd /mnt/fatboy/sauron/kapacitor/conf
docker run --rm kapacitor kapacitord config > kapacitor.conf
cd ~/sauron

# Install systemd service file
sudo cp etc/systemd/kapacitor.service /etc/systemd/system/

# Rescan systemd daemons
sudo systemctl daemon-reload



