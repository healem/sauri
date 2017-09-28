#!/bin/bash

sudo service unifi-video stop
sudo perl -pi -e 's/false/true/g' /mnt/univid/system.properties
sudo rm -rf /mnt/univid/db/*
sudo service unifi-video start

echo "###########################################################################"
echo ""
echo "Now you need to go to the UI and restore the backup"
echo "Once the backup is done, do NOT login - restart the service first"
echo ""
echo "If you can't find a backup, grab one from /mnt/univid/backup"
echo ""
echo "###########################################################################"

