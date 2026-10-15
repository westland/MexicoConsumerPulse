# Hetzner Server Deployment Guide for MexConsumerPulse 🇩🇪 ➔ 🇲🇽

This guide details how to deploy **MexConsumerPulse** on your **Hetzner Cloud VPS** (e.g., CX22, CX32, CPX21, or Dedicated Root Server) running **Ubuntu 22.04 LTS / 24.04 LTS** or **Debian 12**.

---

## ⚡ Option A: Rapid Automated Deployment via Docker (Recommended)

This is the fastest, cleanest method. It containerizes the FastAPI dashboard, headless Chromium browser, and the 24-hour daily scraper scheduler.

### 1. Connect to your Hetzner Server via SSH
```bash
ssh root@<YOUR_HETZNER_IP>
```

### 2. Copy or Clone the Codebase to `/opt/mexconsumerpulse`
If you use Git:
```bash
mkdir -p /opt/mexconsumerpulse
cd /opt/mexconsumerpulse
# Clone your repository or copy via SCP:
# scp -r * root@<YOUR_HETZNER_IP>:/opt/mexconsumerpulse/
```

Or copy files from your local machine using `rsync` or `scp`:
```powershell
# Run from your local Windows terminal:
scp -r "C:\Users\chris\Desktop\Market Research Mexico\*" root@<YOUR_HETZNER_IP>:/opt/mexconsumerpulse/
```

### 3. Run the Automated Deployment Script
```bash
cd /opt/mexconsumerpulse
chmod +x deploy_hetzner.sh
./deploy_hetzner.sh
```

**What the script does automatically:**
1. Updates APT repositories and system packages.
2. Configures UFW firewall (`ports 22, 80, 443, 8000`).
3. Installs Docker and Docker Compose plugin.
4. Builds the container image with Playwright Chromium and dependencies.
5. Launches `mexconsumerpulse_web` (dashboard) and `mexconsumerpulse_scheduler` (daily background agent).

### 4. Access the Live Web Application
Open your browser and navigate to:
```
http://<YOUR_HETZNER_IP>:8000
```

---

## 🛠️ Option B: Native Deployment (Systemd + Nginx)

If you prefer running directly on the Linux host without Docker:

### 1. Install System Dependencies & Playwright
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx

# Create directory and virtual environment
sudo mkdir -p /opt/mexconsumerpulse
cd /opt/mexconsumerpulse
python3 -m venv venv
source venv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Install Playwright Chromium with Linux OS libraries
playwright install --with-deps chromium
```

### 2. Install Systemd Services
Copy the provided service unit files:
```bash
sudo cp hetzner/systemd/mexconsumerpulse.service /etc/systemd/system/
sudo cp hetzner/systemd/mexconsumerpulse-scheduler.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now mexconsumerpulse
sudo systemctl enable --now mexconsumerpulse-scheduler
```

Verify service status:
```bash
sudo systemctl status mexconsumerpulse
sudo systemctl status mexconsumerpulse-scheduler
```

### 3. Setup Nginx Reverse Proxy & Free SSL (Let's Encrypt)
```bash
sudo cp hetzner/nginx/mexconsumerpulse.conf /etc/nginx/sites-available/mexconsumerpulse
sudo ln -s /etc/nginx/sites-available/mexconsumerpulse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

If you have a domain pointed to your Hetzner IP:
```bash
sudo certbot --nginx -d pulse.yourdomain.com
```

---

## 👥 Handling Facebook 2FA & Session on a Headless Server

Because your Hetzner server is headless (no physical monitor attached):
1. **Option 1 (Easiest)**: Run `python run.py --fb-login` once on your **local computer**. This generates `data/auth_state/facebook_state.json`.
2. Copy that single JSON file to your Hetzner server:
   ```bash
   scp data/auth_state/facebook_state.json root@<YOUR_HETZNER_IP>:/opt/mexconsumerpulse/data/auth_state/
   ```
3. The server container/daemon will automatically use the active session cookies without ever asking for login again!

---

## 📊 Useful Server Commands

```bash
# View live web dashboard logs
docker compose logs -f web

# View live daily scraper execution logs
docker compose logs -f scheduler

# Trigger an on-demand complete research run right now
docker compose exec web python run.py --all

# Download the latest CSV export to your local computer
scp root@<YOUR_HETZNER_IP>:/opt/mexconsumerpulse/data/exports/mexico_consumer_problems_latest.csv .
```
