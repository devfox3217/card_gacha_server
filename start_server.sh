#!/bin/bash

echo "Installing required Python packages..."
pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography]

echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
