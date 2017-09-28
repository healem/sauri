#!/bin/bash

sudo service unifi-controller stop
sudo perl -pi -e 's/false/true/g' /mnt/unifictl/system.properties
sudo rm -rf /mnt/unifictl/db/*
sudo service unifi-controller start

