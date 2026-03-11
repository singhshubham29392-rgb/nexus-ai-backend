#!/bin/bash
# Production Deployment Script for Nexus AI Backend
# Run this on your production server
# Usage: bash setup_production.sh

set -e  # Exit on error

echo "=================================="
echo "Nexus AI Backend - Production Setup"
echo "=================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "⚠️  This script should be run with sudo for system packages"
  echo "Continue anyway? (y/n)"
  read -r response
  if [[ ! $response =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Step 1: Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Step 2: Install Python dependencies
echo "🐍 Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Step 3: Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    curl \
    wget \
    git \
    supervisor \
    nginx

# Step 4: Create application directory
APP_DIR="/var/www/nexus-ai-backend"
echo "📂 Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR

# Step 5: Clone repository
echo "📥 Cloning repository..."
cd $APP_DIR
git clone <YOUR_REPO_URL> . 2>/dev/null || git pull

# Step 6: Create virtual environment
echo "🔐 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Step 7: Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn

# Step 8: Create .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Nexus AI Backend Production Configuration
ENVIRONMENT=production
DEBUG=false

SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=info

# Set these values with actual credentials
GEMINI_API_KEY=your_gemini_api_key_here
FIREBASE_CREDENTIALS_PATH=$APP_DIR/serviceAccountKey.json
GEMINI_MODEL_NAME=gemini-1.5-flash

# Frontend
FRONTEND_URL=https://yourdomain.com
EOF
    echo "⚠️  Please edit .env file with your credentials:"
    echo "   nano $APP_DIR/.env"
    exit 1
fi

# Step 9: Create systemd service file
echo "🚀 Creating systemd service..."
sudo tee /etc/systemd/system/nexus-ai-backend.service > /dev/null << EOF
[Unit]
Description=Nexus AI Backend Service
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 10: Enable and start service
echo "✅ Enabling Nexus AI service..."
sudo systemctl daemon-reload
sudo systemctl enable nexus-ai-backend.service

# Step 11: Configure Nginx reverse proxy
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/nexus-ai-backend > /dev/null << 'EOF'
upstream nexus_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;

    location / {
        proxy_pass http://nexus_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/nexus-ai-backend /etc/nginx/sites-enabled/ || true
sudo rm -f /etc/nginx/sites-enabled/default

# Step 12: Test and enable Nginx
echo "✅ Testing and enabling Nginx..."
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# Step 13: Setup SSL with Let's Encrypt
echo "🔒 Setting up HTTPS with Let's Encrypt..."
echo ""
echo "Before continuing, make sure:"
echo "1. Your domain is pointing to this server's IP"
echo "2. HTTP:80 and HTTPS:443 are open in firewall"
echo ""
read -p "Continue with HTTPS setup? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo apt-get install -y certbot python3-certbot-nginx
    echo "Replace yourdomain.com with your actual domain:"
    read -p "Domain: " DOMAIN
    sudo certbot --nginx -d $DOMAIN --agree-tos --email admin@$DOMAIN -n
fi

# Step 14: Create log directory
echo "📋 Setting up logging..."
mkdir -p logs
chmod 755 logs

# Step 15: Test the service
echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your credentials:"
echo "   nano $APP_DIR/.env"
echo ""
echo "2. Add Firebase serviceAccountKey.json:"
echo "   Copy your serviceAccountKey.json to $APP_DIR/"
echo ""
echo "3. Start the service:"
echo "   sudo systemctl start nexus-ai-backend"
echo ""
echo "4. Check service status:"
echo "   sudo systemctl status nexus-ai-backend"
echo ""
echo "5. View logs:"
echo "   sudo journalctl -u nexus-ai-backend -f"
echo ""
echo "6. Update Nginx domain:"
echo "   sudo nano /etc/nginx/sites-available/nexus-ai-backend"
echo "   (Replace yourdomain.com with your domain)"
echo ""
echo "Your API will be available at:"
echo "   https://yourdomain.com/agent/analyze-task"
echo ""
