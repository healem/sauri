#!/bin/bash

coverage run -m --omit=/home/healem/envs/* --omit=/usr/local/* unittest discover --pattern=test*.py
coverage report -m
