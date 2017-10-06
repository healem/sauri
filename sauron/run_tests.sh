#!/bin/bash

coverage run -m --omit=/home/healem/projects/automation/sauron/sauron/lib/* unittest discover --pattern=test*.py
coverage report -m
