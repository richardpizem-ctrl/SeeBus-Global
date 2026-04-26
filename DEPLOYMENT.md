# DEPLOYMENT – SeeBus‑Global

This document describes how to deploy the SeeBus‑Global backend in local, staging, and production environments.  
The deployment process is designed to be simple, predictable, and stable.

---------------------------------------

## 1. Requirements

### Runtime
- Python 3.10+
- pip or uv package manager
- Linux or Windows environment

### System
- Minimum 1 CPU core
- 512 MB RAM
- Stable internet connection for GTFS‑RT feeds

### Files
- Static GTFS dataset (routes, stops, trips…)
- config.yaml (optional but recommended)

---------------------------------------

## 2. Directory Structure

Recommended structure for deployment:

/seebus-global  
  /app  
  /data  
    /gtfs_static  
  /logs  
  config.yaml  
  run.sh  
  venv/ (optional)

---------------------------------------

## 3. Installation

### Using pip
pip install -r requirements.txt

### Using uv (recommended)
uv sync

---------------------------------------

## 4. Environment Setup

Set required environment variables:

export SEEBUS_PORT=8080  
export GTFS_STATIC_PATH=./data/gtfs_static/  
export GTFS_RT_URL=https://transit.example.com/gtfs-rt/tripupdates  

Optional:

export CACHE_TTL_SECONDS=30  
export ANNOUNCEMENTS_LANGUAGE=en  
export ANNOUNCEMENTS_VERBOSITY=medium  
export ENABLE_TTS=true  

---------------------------------------

## 5. Starting the Server

### Development mode
python main.py

### Production mode (recommended)
Use a process manager:

#### systemd
[Unit]
Description=SeeBus-Global Backend

[Service]
WorkingDirectory=/seebus-global
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target

systemctl enable seebus  
systemctl start seebus

#### PM2 (Node-based process manager)
pm2 start "python3 main.py" --name seebus  
pm2 save

---------------------------------------

## 6. Reverse Proxy (Production)

### Nginx example
server {
    listen 80;
    server_name seebus.example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Reload:
nginx -s reload

---------------------------------------

## 7. Logging

Logs are written to the file defined in config.yaml:

logging:
  level: "info"
  file: "./logs/seebus.log"

Rotate logs using logrotate:

/logs/seebus.log {
    daily
    rotate 7
    compress
    missingok
}

---------------------------------------

## 8. Updating the Deployment

### Pull latest changes
git pull origin main

### Reinstall dependencies
uv sync  
or  
pip install -r requirements.txt

### Restart service
systemctl restart seebus  
or  
pm2 restart seebus

---------------------------------------

## 9. Health Check

Verify backend is running:

curl http://localhost:8080/status

Expected response:
{ "status": "ok" }

---------------------------------------

## 10. Backup Strategy

Backup the following:

- config.yaml  
- /data/gtfs_static  
- /logs (optional)  
- git repository (optional)

---------------------------------------

## 11. Troubleshooting

### Server does not start
- Check missing GTFS files  
- Check invalid YAML format  
- Check port availability  

### GTFS‑RT not updating
- Verify GTFS_RT_URL  
- Check internet connection  
- Check provider feed status  

---------------------------------------

# End of file
