from fastapi import FastAPI

from easy_auth.routers.get_jwks import router as jwks_router

app = FastAPI()

app.include_router(jwks_router)

# {
#   "iss": "https://auth.benbest.uk",
#   "sub": "<uuid>",
#   "aud": "<client_id>",
#   "roles": ["admin"],
#   "exp": <epoch_seconds>,
#   "iat": <epoch_seconds>,
#   "email_verified": <bool>
# }

# Endpoints

# Well know keys - GET route
# @app.get("/.well-known/jwks.json")
# User can get public key from here

# Register - POST route
# @app.post("/auth/register")
# User send email and password and client_id
# Check client - unknown -> reject
# Parse json body
# Hash password
# If dupe email, send "someone tried to use your email", return same response
# Write to DB with email_verified = 0 and
# create membership row (client_id x user x role) (one transaction)
# Create JWT token
# Send access token in res body
# Refresh token in __Host- cookie

# Verify email - POST route
# @app.post("/auth/verify-email")
# Link in email sends single-use short-lived hashed token
# Once verified - update flag in user db

# Login - POST route
# @app.post("auth/login")
# User send email and password and client_id
# Parse body
# Check client - unknown -> reject
# Compare password against stored (use dummy hash if user doesnt exist)\
# 401 if user doesnt exist or password wrong
# Check membership row - reject if not member
# Create JWT token
# Send access token in res body
# Refresh token in __Host- cookie

# Refresh token - POST route
# @app.post("auth/refresh")
# Get refresh token from cookie, needs client_id as well
# If refresh token already used, revoke family and don't refresh
# Re-validate membership
# Generate new access token, send in res body
# Issue new refresh token, set in cookie
# Invalidate old refresh token

# Logout - POST route
# @app.post("auth/logout")
# Revoke refresh tokens for this sessions family
# Clear Auth cookie with 200

# Me - GET route
# @app.get("/auth/userinfo")
# Needs valid access token
# Derive user id from tokens sub
# Returns email


# DB schemas

# # Users tables
# user_id - unique uuid, non null, PK
# email - unique, non null, unique index on lower(email)
# password_hash - full argon2 encoded string, nun null
# email_verified - bool, default = 0
# created_at - timestamp
# updated_at - timestamp, null

# # Clients table
# client_id - unique, non null, PK
# name - text
# allowed redirect origins - list, null
# auto_provision - bool, default = 1
# CORS origin - lisy
# secret hash - null
# created_at - timestamp, not null
# is_active - bool, default = 1

# # Memberships
# client_id - non-null
# user_id - non-null
# role - non-null, default = "user"
# created_at - timestamp, not null

# composite key on client and user
# cascade on user and client deletion

# # Refresh tokens
# token_hash - unique, non null, PK
# user_id - FK, index
# family_id - non-null, index
# used_at - default = null, update when used
# token_exp - timestamp, expiry
# revoked_at - null, timestamp, delete after a few days
# created_at - timestamp
# family_expires_at - timestamp
