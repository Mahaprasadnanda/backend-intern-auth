import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
import jwt

app = FastAPI()

# Secret keys (we use env variables in production)
SECRET_KEY = os.getenv("SECRET_KEY", "your_jwt_secret_key")
SESSION_SECRET = os.getenv("SESSION_SECRET", "your_session_secret_key")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "958126175250-37k0uat69qiuii0h7fd6c5aibjprapt3.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "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")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# OAuth configuration
config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
    "SECRET_KEY": SESSION_SECRET
}
config = Config(environ=config_data)

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Dummy data
dummy_posts = [
    {"post_id": 1, "title": "First Post", "contentSnippet": "Hello World!"},
    {"post_id": 2, "title": "Second Post", "contentSnippet": "FastAPI is awesome!"},
]

# JWT dependency
bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Routes

@app.get("/")
def home():
    return {"message": "Welcome to LawVriksh API"}

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    try:
        # Fetch token from Google
        token = await oauth.google.authorize_access_token(request)
        print("OAuth Token:", token)

        # Try to get userinfo from token
        user = token.get("userinfo")
        if not user:
            # fallback: decode id_token manually (no signature verification for demo)
            import jwt as pyjwt
            id_token = token.get("id_token")
            if not id_token:
                raise Exception("No id_token in token response")
            user = pyjwt.decode(id_token, options={"verify_signature": False})

        print("User Info:", user)

        # Encode JWT token for FastAPI
        jwt_token = jwt.encode({"sub": user["email"]}, SECRET_KEY, algorithm="HS256")

        # Return access token
        return JSONResponse({
            "access_token": jwt_token,
            "token_type": "bearer",
            "user_email": user["email"]
        })

    except Exception as e:
        print("OAuth Error:", str(e))
        return JSONResponse({
            "error": "OAuth authentication failed",
            "details": str(e)
        }, status_code=500)

@app.get("/api/posts")
def get_posts(user=Depends(get_current_user)):
    return {"user": user["sub"], "posts": dummy_posts}
