from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "*", # Allows all connections - perfect for local Wi-Fi demos
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )