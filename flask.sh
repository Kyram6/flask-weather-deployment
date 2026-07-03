#!/bin/bash

#------- system update 
sudo apt update -y
sudo apt upgrade -y

#------ install dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

#------ configure nginix 
sudo sed -i 's|try_files \$uri \$uri/ =404;|proxy_pass http://127.0.0.1:5000;|' /etc/nginx/sites-available/default
sudo systemctl restart nginx

#------ set up virtual environmenr
cd /home/ubuntu
python3 -m venv venv

#------ install inside venv
./venv/bin/pip pip install flask requests gunicorn

#------ set environment variable
export WEATHER_API_KEY="8792c2a1ce7d49520f4f7e904db607dc"

#------ Run flask with gunicorn
./venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 weather_flask:app


