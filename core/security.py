"""
Security module for Nexus AI Backend.
Handles CORS and other security configurations.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
        
    Note:
        - In production, restrict origins to specific domains
        - For development, localhost and common ports are allowed
    """
    # Development origins
    allowed_origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Add frontend URL from environment if specified
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        allowed_origins.append(frontend_url)
    
    # Restrict in production
    if os.getenv("ENVIRONMENT", "development").lower() == "production":
        if not frontend_url:
            raise ValueError(
                "FRONTEND_URL must be set in production environment"
            )
        allowed_origins = [frontend_url]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )