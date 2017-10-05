#!/bin/bash

coverage run -m --omit=/home/healem/projects/automation/sauron/sauron/lib/* sensors.temperature.test.testds18b20
coverage report -m
