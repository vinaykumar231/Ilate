
# ####################################################################################
# from fastapi import FastAPI, Request, Depends, HTTPException, APIRouter
# from authlib.integrations.starlette_client import OAuth
# from starlette.middleware.sessions import SessionMiddleware
# from fastapi.responses import RedirectResponse,JSONResponse
# from sqlalchemy.orm import Session
# import secrets
# ##################################################################################

# router = APIRouter()
# # Initialize FastAPI app
# app = FastAPI()

# # Generate a secure random string for the SessionMiddleware secret key
# SECRET_KEY = "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"
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# # OAuth configuration
# oauth = OAuth()
# oauth.register(
#     name='google',
#     client_id="1060983306336-bg15c4kcvbd51jjj0p08pd68rp7uis6l.apps.googleusercontent.com",
#     client_secret="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",
#     server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
#     client_kwargs={'scope': 'openid email profile'}
# )

# # Google login endpoint
# @router.get("/login11")
# async def google_login(request: Request):
#     redirect_uri = request.url_for('auth')
#     return await oauth.google.authorize_redirect(request, redirect_uri)

# # Google callback endpoint
# @router.get("/auth")
# async def auth(request: Request):
#     try:
#         # Retrieve the token and user information
#         token = await oauth.google.authorize_access_token(request)
#         user = await oauth.google.parse_id_token(request, token)
        
#         # Handle authenticated user data here
#         # Example:
#         # db_user = db.query(User).filter(User.email == user['email']).first()
#         # if not db_user:
#         #     db_user = User(email=user['email'], name=user['name'])
#         #     db.add(db_user)
#         #     db.commit()

#         # After handling user data, redirect to a success page or home page
#         return JSONResponse(content={"user":user})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Google authentication failed")

