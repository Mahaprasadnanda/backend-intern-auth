# LawVriksh Backend Intern Assignment 1

This project implements a secure backend API using FastAPI, with Google OAuth authentication and a protected sample data endpoint.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables (recommended):
   - On Windows (PowerShell):
     ```powershell
     $env:SECRET_KEY="your_jwt_secret_key"
     $env:SESSION_SECRET="your_session_secret_key"
     $env:GOOGLE_CLIENT_ID="your_google_client_id"
     $env:GOOGLE_CLIENT_SECRET="your_google_client_secret"
     ```
   - On Linux/macOS:
     ```bash
     export SECRET_KEY=your_jwt_secret_key
     export SESSION_SECRET=your_session_secret_key
     export GOOGLE_CLIENT_ID=your_google_client_id
     export GOOGLE_CLIENT_SECRET=your_google_client_secret
     ```
   - Or edit directly in `main.py` for demo.
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Google OAuth Setup
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new OAuth 2.0 Client ID (Web application)
- Set Authorized redirect URI to: `http://localhost:8000/auth`
- Copy the client ID and secret into your environment or `main.py`

## API Endpoints
- `/login`: Redirects to Google for authentication
- `/auth`: Handles Google callback, returns JWT
- `/api/posts`: Protected endpoint, requires Bearer JWT in `Authorization` header

## Example Usage
1. Visit `http://localhost:8000/login` in the browser and authenticate with Google.
2. Copy the `access_token` from the response.
3. Make a GET request to `/api/posts` with header:
   ```
   Authorization: Bearer <access_token>
   ```

## Linting
Run `flake8` in the `assignment1/` directory.

## Postman Collection
- See `postman_collection.json` in this folder for demo requests and flows.