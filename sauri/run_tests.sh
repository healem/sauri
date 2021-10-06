#!/bin/bash

coverage run -m --omit=/home/healem/envs/* --omit=/usr/* unittest discover --pattern=test*.py
coverage report -m
