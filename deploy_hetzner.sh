#!/usr/bin/env bash
# ==============================================================================
# MexConsumerPulse - Automated Hetzner Server Deployment Script
# Supports: Ubuntu 22.04 / 24.04 LTS & Debian 11 / 12 on Hetzner Cloud
# ==============================================================================

set -euo pipefail

echo "======================================================================"
echo " 🇲🇽 DEPLOYING MEXCONSUMERPULSE TO HETZNER SERVER"
echo " Target: Autonomous Mexican Consumer Market Research Swarm"
echo "======================================================================"

# 1. Update OS Packages
echo "\n[1/5] Updating system packages..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends curl wget git ufw apt-transport-https ca-certificates gnupg lsb-release

# 2. Configure UFW Firewall
echo "\n[2/5] Configuring firewall (UFW)..."
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw allow 8000/tcp comment 'Internal Services'
ufw allow 8080/tcp comment 'MexConsumerPulse Dashboard'
ufw --force enable

# 3. Install Docker & Docker Compose if not present
if ! command -v docker &> /dev/null; then
    echo "\n[3/5] Installing Docker..."
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "\n[3/5] Docker is already installed."
fi

# 4. Prepare Directories and Permissions
echo "\n[4/5] Setting up persistent storage..."
mkdir -p data/auth_state data/exports reports/daily_reports
chmod -R 755 data reports

# 5. Build and Launch Containers
echo "\n[5/5] Building and launching Docker containers..."
docker compose down || true
docker compose up -d --build

SERVER_IP=$(curl -s -4 ifconfig.me || hostname -I | awk '{print $1}')

echo "\n======================================================================"
echo " 🎉 MEXCONSUMERPULSE DEPLOYED SUCCESSFULLY ON HETZNER!"
echo "======================================================================"
echo " Web Dashboard URL: http://${SERVER_IP}:8080"
echo " API Docs URL:     http://${SERVER_IP}:8080/docs"
echo ""
echo " Useful Maintenance Commands:"
echo " - View container logs:   docker compose logs -f"
echo " - View web logs:         docker compose logs -f web"
echo " - View scraper logs:     docker compose logs -f scheduler"
echo " - Trigger immediate run: docker compose exec web python run.py --all"
echo " - Stop services:         docker compose down"
echo "======================================================================"
