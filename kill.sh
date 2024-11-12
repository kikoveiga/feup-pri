#!/bin/bash

sudo docker rm -f $(sudo docker ps -aq)
sudo docker ps
