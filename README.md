# Nexus AI Backend

A FastAPI-based backend for AI-powered task analysis and project management, powered by Google's Gemini AI and Firebase.

## Features

- 🤖 AI Task Analysis using Google Gemini
- 📊 Firebase Integration for data persistence
- ⚡ FastAPI for high-performance API endpoints
- 🔐 Environment-based configuration
- 🛡️ CORS security middleware
- 📝 Comprehensive logging

## Prerequisites

- Python 3.8+
- Firebase Service Account Key
- Google Gemini API Key

## Setup Instructions

### 1. Clone the Repository and Navigate to Project

```bash
cd nexus_backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
- `GEMINI_API_KEY`: Your Google Gemini API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)
- `FIREBASE_CREDENTIALS_PATH`: Path to your Firebase service account key JSON file
- `FRONTEND_URL`: Your frontend URL (for CORS)

### 5. Add Firebase Credentials

Place your `serviceAccountKey.json` file in the project root directory.

## Running the Application

### Development

```bash
python main.py
```

or with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env
```

or with Gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## API Endpoints

### Health Check
- **GET** `/`  
  Returns server status and version

### Task Analysis
- **POST** `/agent/analyze-task`  
  Analyze a task using Gemini AI  
  Body: `{ "description": "your task description" }`

### Task History  
- **GET** `/agent/history`  
  Retrieve all analyzed tasks from Firebase

## Project Structure

```
nexus_backend/
├── agents/
│   ├── __init__.py
│   └── task_agent.py          # AI agent for task analysis
├── core/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── constants.py           # Application constants
│   └── security.py            # CORS and security setup
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── serviceAccountKey.json    # Firebase credentials (DO NOT COMMIT)
└── README.md                 # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API Key | Yes |
| `FIREBASE_CREDENTIALS_PATH` | Path to Firebase service account key | Yes |
| `GEMINI_MODEL_NAME` | Gemini model to use | No (default: gemini-1.5-flash) |
| `ENVIRONMENT` | Environment (development/production) | No (default: development) |
| `DEBUG` | Enable debug mode | No (default: false) |
| `SERVER_HOST` | Server host | No (default: 0.0.0.0) |
| `SERVER_PORT` | Server port | No (default: 8000) |
| `LOG_LEVEL` | Logging level | No (default: info) |
| `FRONTEND_URL` | Frontend URL for CORS | No |

## Security Recommendations

### Before Deployment:

1. ✅ **Never commit sensitive files:**
   - `.env` file
   - `serviceAccountKey.json`
   - Any API keys

2. ✅ **Set restricted CORS origins** in production:
   - Edit `core/security.py`
   - Specify exact frontend domain
   - Avoid using `"*"` in production

3. ✅ **Use environment variables** for all sensitive data:
   - API keys
   - Database credentials
   - Secret tokens

4. ✅ **Enable HTTPS** in production

5. ✅ **Implement rate limiting** for API endpoints

6. ✅ **Use health checks** for monitoring

## Deployment

### Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t nexus-ai-backend .
docker run -p 8000:8000 --env-file .env nexus-ai-backend
```

### Cloud Deployment (AWS/GCP/Azure)

1. Set environment variables in your cloud platform
2. Upload code to your repository
3. Deploy using your platform's deployment service
4. Ensure Firebase and Gemini credentials are set as environment variables

## Troubleshooting

### Firebase Connection Error
- Verify `serviceAccountKey.json` exists and is valid
- Check `FIREBASE_CREDENTIALS_PATH` in `.env`

### Gemini API Errors
- Verify `GEMINI_API_KEY` is correct
- Ensure API is enabled in Google Cloud Console
- Check rate limits and quota

### CORS Errors
- Add frontend URL to `FRONTEND_URL` env variable
- For development, ensure origins include your frontend domain

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

## Logging

Logs are configured to output:
- Console output with formatted timestamps
- Configurable log levels via `LOG_LEVEL` environment variable

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.
