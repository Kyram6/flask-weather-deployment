# Flask Weather API — Deployment Guide

Deploys a Flask weather-lookup app (postcode → coordinates → weather) to an EC2 instance, served via Gunicorn behind Nginx.

**Replace `<IP>` throughout with your instance's public IP address.**

---

## 1. Launch EC2

| Setting | Value |
|---|---|
| Instance type | t3.micro |
| OS | Ubuntu 24.04 LTS |
| Security group | SSH (22), HTTP (80) |

---

## 2. Copy files to EC2

Run these from your **local Mac terminal** (not SSH'd into the VM).

**Copy the Flask app:**
```bash
scp -i ~/.ssh/kyram-tech610-key.pem \
  /Users/kyramngoma/Tech610/DevOpsPython/App/weather_flask.py \
  ubuntu@<IP>:/home/ubuntu/
```

**Copy the deploy script:**
```bash
scp -i ~/.ssh/kyram-tech610-key.pem \
  /Users/kyramngoma/Tech610/Cloud/flask.sh \
  ubuntu@<IP>:/home/ubuntu/
```

**Copy the templates folder** (note the `-r` flag — required for directories):
```bash
scp -i ~/.ssh/kyram-tech610-key.pem -r \
  /Users/kyramngoma/Tech610/DevOpsPython/App/templates \
  ubuntu@<IP>:/home/ubuntu/
```

> **Tip:** after copying, verify the file sizes match on both sides with `ls -la` (Mac) and `ls -la` (VM) — a 0-byte or mismatched file is the most common cause of a blank page or 500 error.

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

## Deploy script — `flask.sh`

```bash
#!/bin/bash
```

### 1. Update system
```bash
sudo apt update -y
sudo apt upgrade -y
```

### 2. Install dependencies
- `python3-venv` — isolates Python packages per project
- `nginx` — web server used as a reverse proxy

```bash
sudo apt install python3 python3-pip python3-venv nginx -y
```

### 3. Configure Nginx as a reverse proxy
Forwards port 80 traffic to Flask on port 5000, so users visit `http://<IP>/` instead of `http://<IP>:5000/`.

```bash
sudo sed -i 's|try_files \$uri \$uri/ =404;|proxy_pass http://127.0.0.1:5000;|' /etc/nginx/sites-available/default
sudo systemctl restart nginx
```

### 4. Set up app directory
```bash
cd /home/ubuntu
```

### 5. Create virtual environment
```bash
python3 -m venv venv
```

### 6. Install Python packages inside the venv
Must use `./venv/bin/pip` (not plain `pip`) so packages install into the venv, not system Python.

```bash
./venv/bin/pip install flask requests gunicorn
```

### 7. Set the API key as an environment variable
Using an env var instead of a hardcoded key or file path means the app works on any machine without code changes.

```bash
export WEATHER_API_KEY="your_api_key_here"
```

> **Security note:** don't commit a real key into `flask.sh` or this doc

### 8. Start the app with Gunicorn
- `-w 4` — 4 worker processes
- `-b 127.0.0.1:5000` — binds to localhost only; Nginx handles public traffic on port 80
- `weather_flask:app` — `<filename>:<Flask object name>`

```bash
./venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 weather_flask:app
```

---

## Accessing the app

| Purpose | URL |
|---|---|
| Web UI | `http://<IP>/` |
| Weather API (JSON) | `http://<IP>/weather/<postcode>` |

`/weather/<postcode>` is an API endpoint mine returns raw JSON. That's expected behavior, not a bug. WIP.

**Screenshots:**

![Homepage](screenshots/homepage.png)

![Weather result](screenshots/weather-result.png)



