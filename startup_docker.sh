#!/bin/bash
sudo docker build -t habr-proxy .
sudo docker run --name habr-proxy -p 8080:8080 -it habr-proxy:latest
