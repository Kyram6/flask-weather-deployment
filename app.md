# Flask Weather API — Deployment Guide

## 1. Launch EC2

- Instance type: t3.micro
- OS: Ubuntu 24.04 LTS
- Security group: SSH (22), HTTP (80)

---

## 2. Copy files to EC2

Run these on local Mac:


Copy Flask app
```
scp -i ~/.ssh/kyram-tech610-key.pem /Users/kyramngoma/Tech610/DevOpsPython/App/weather_flask.py ubuntu@<IP>:/home/ubuntu/
```

Copy deploy script
```
scp -i ~/.ssh/kyram-tech610-key.pem /Users/kyramngoma/Tech610/Cloud/flask.sh ubuntu@<IP>:/home/ubuntu/
```

---

## 3. SSH in

```bash
ssh -i ~/.ssh/kyram-tech610-key.pem ubuntu@<IP>
```

---

## 4. Run the deploy script

```bash
chmod +x flask.sh
./flask.sh
```

---

# Deploy script — flask.sh

```
#!/bin/bash 
```

## 1. Update system
```
sudo apt update -y
sudo apt upgrade -y
```

## 2. Install dependencies
- python3-venv: isolates Python packages per project
- nginx: web server used as reverse proxy
```
sudo apt install python3 python3-pip python3-venv nginx -y
```

## 3. Configure Nginx as reverse proxy
- Forwards port 80 traffic to Flask on port 5000
- so users visit http://<IP> instead of http://<IP>:5000
```
sudo sed -i 's|try_files \$uri \$uri/ =404;|proxy_pass http://127.0.0.1:5000;|' /etc/nginx/sites-available/default
```
```
sudo systemctl restart nginx
```

## 4. Set up app directory
```
cd /home/ubuntu
```

## 5. Create virtual environment
```
python3 -m venv venv
```

## 6. Install Python packages inside venv
- so packages go into venv, not system Python

```
./venv/bin/pip install flask requests gunicorn
```

## 7. Set API key as environment variable
Using an env var instead of a file path means the app works on any machine
```
export WEATHER_API_KEY="your_api_key_here"
```

## 8. Start app with Gunicorn
-  -w 4: 4 worker processes
-  -b 127.0.0.1:5000: localhost only, Nginx handles public traffic
-  weather_flask:app = filename:Flask object name
```
./venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 weather_flask:app
```



---

## Accessing the app

http://[IP]/

http://[IP]/weather/[POSTCODE]
