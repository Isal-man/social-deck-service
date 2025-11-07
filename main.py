import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from config import settings

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

oauth = OAuth()

oauth.register(
    name='twitter',
    client_id=settings.X_CLIENT_ID,
    client_secret=settings.X_CLIENT_SECRET,
    authorize_url='https://twitter.com/i/oauth2/authorize',
    access_token_url='https://api.twitter.com/2/oauth2/token',
    client_kwargs={
        'scope': 'tweet.read tweet.write users.read offline.access'
    }
)

@app.get("/auth/twitter/login")
async def twitter_login(request: Request):
    redirect_uri = request.url_for('twitter_callback')
    
    print(f"Callback URI yang di-generate: {redirect_uri}")
    
    return await oauth.twitter.authorize_redirect(request, redirect_uri)

@app.get("/auth/twitter/callback")
async def twitter_callback(request: Request):
    try:
        token = await oauth.twitter.authorize_access_token(request)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Oauth failed", "details": str(e)}
        )
        
    access_token = token.get('access_token')
    refresh_token = token.get('refresh_token')
    
    print("---   TOKEN DITERIMA   ---")
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
    print("------------------------------------")
    
    return JSONResponse(
        content={
            "message": "Sukses terhubung dengan Twitter!"
        }
    )
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)