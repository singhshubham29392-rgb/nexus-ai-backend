"""
Deployment Configuration Guide for Nexus AI Backend
Follow these steps to safely deploy to production
"""

# DEPLOYMENT CHECKLIST
"""
Before Deploying to Server:

✅ SECURITY
  □ Remove all hardcoded API keys
  □ Set GEMINI_API_KEY as environment variable
  □ Store Firebase credentials as environment variable
  □ Set .gitignore to never commit secrets
  □ Use .env.example as template (never commit .env)

✅ CONFIGURATION
  □ Create .env file on server with:
    - GEMINI_API_KEY=<your_key>
    - FIREBASE_CREDENTIALS_PATH=<path_to_credentials>
    - ENVIRONMENT=production
    - FRONTEND_URL=<your_frontend_domain>
    - DEBUG=false

✅ DEPENDENCIES
  □ Run: pip install -r requirements.txt
  □ Verify all packages installed: pip list
  □ Check Python version: python --version (3.8+)

✅ FIREBASE
  □ Place serviceAccountKey.json in project root
  □ Or set FIREBASE_CREDENTIALS_PATH to full path
  □ Test connection with: python -c "import firebase_admin; print('OK')"

✅ CORS SECURITY
  □ Update FRONTEND_URL environment variable
  □ Verify allowed_origins in core/security.py
  □ Remove wildcard "*" from production origins

✅ TESTING
  □ Start server: python run.py
  □ Test health endpoint: curl http://localhost:8000/
  □ Response should include: "status": "Nexus AI Server is Live"

✅ LOGGING
  □ Set LOG_LEVEL=info for production
  □ Monitor logs for errors: tail -f logs/app.log
  □ Verify no sensitive data in logs

✅ PRODUCTION SERVER
  □ Use Gunicorn or uWSGI (not uvicorn alone)
  □ Example: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
  □ Or with Docker for containerization
"""

# ENVIRONMENT VARIABLES REQUIRED
"""
Production .env file must contain:

# CRITICAL
GEMINI_API_KEY=your_actual_gemini_api_key_here
FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccountKey.json

# RECOMMENDED  
ENVIRONMENT=production
DEBUG=false
FRONTEND_URL=https://yourdomain.com
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=info
GEMINI_MODEL_NAME=gemini-1.5-flash
"""

# DEPLOYMENT METHODS

# Method 1: Direct Server (Linux/macOS)
"""
1. SSH into server
2. Clone repository
3. Create virtual environment:
   python -m venv .venv
   source .venv/bin/activate

4. Create .env file with production values
5. Install dependencies:
   pip install -r requirements.txt

6. Run with Gunicorn:
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

7. Use systemd or supervisor to keep running
"""

# Method 2: Docker Deployment
"""
Dockerfile content:

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Build:
docker build -t nexus-ai-backend:latest .

Run:
docker run -d \
  --name nexus-backend \
  -p 8000:8000 \
  --env-file .env \
  nexus-ai-backend:latest
"""

# Method 3: Heroku Deployment
"""
1. Create Procfile:
   web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

2. Set environment variables:
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set FIREBASE_CREDENTIALS_PATH=...

3. Deploy:
   git push heroku main
"""

# COMMON ISSUES & SOLUTIONS

"""
Issue: "GEMINI_API_KEY not set"
Solution: Set environment variable before running server

Issue: "Firebase credentials file not found"
Solution: Use correct FIREBASE_CREDENTIALS_PATH or place file in root

Issue: "Port 8000 already in use"
Solution: Change SERVER_PORT environment variable or kill process

Issue: "CORS error in frontend"
Solution: Set FRONTEND_URL environment variable to your domain

Issue: "Connection refused from frontend"
Solution: Verify server IP, port, and CORS configuration
"""

# POST-DEPLOYMENT

"""
After deploying:

1. Test API endpoints:
   curl http://your-server:8000/
   curl -X POST http://your-server:8000/agent/analyze-task \
     -H "Content-Type: application/json" \
     -d '{"description": "test task"}'

2. Monitor logs for errors:
   tail -f /path/to/logs/app.log

3. Set up health checks:
   Use uptime monitoring service
   Check http://your-server:8000/ regularly

4. Enable HTTPS:
   Use Let's Encrypt with nginx reverse proxy
   Install certbot: sudo apt install certbot python3-certbot-nginx
   Obtain cert: sudo certbot certonly --nginx -d yourdomain.com

5. Set up reverse proxy (nginx example):
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
"""
