from fastapi import FastAPI, Header, Body, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from . import models, database, auth
import os
import httpx
from dotenv import load_dotenv

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Example data model
class Message(BaseModel):
    content: str
    priority: Optional[int] = 1

# Pydantic models
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages")
MCP_UPLOAD_URL = os.getenv("MCP_UPLOAD_URL", "https://api.anthropic.com/v1/mcp/upload")

# Authentication endpoints
@app.post("/api/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(database.get_db)):
    try:
        # Check if user already exists
        db_user = db.query(models.User).filter(
            (models.User.email == user.email) | 
            (models.User.username == user.username)
        ).first()
        
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create new user
        hashed_password = auth.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.username == form_data.username).first()
        if not user or not auth.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = auth.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/users/me", response_model=UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/api/analyze-campaign/")
async def analyze_campaign(
    file: UploadFile = File(...),
    details: str = Form(...)
):
    # 1. Upload CSV to local MCP server
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    files = {"file": (file.filename, await file.read(), file.content_type or "text/csv")}
    try:
        async with httpx.AsyncClient() as client:
            mcp_resp = await client.post("http://localhost:8000/api/mcp-upload/", headers=headers, files=files)
            mcp_resp.raise_for_status()
            context_id = mcp_resp.json()["context_id"]
            print(f"[DEBUG] MCP upload response: {mcp_resp.json()}")
    except Exception as e:
        print(f"[DEBUG] MCP upload error: {e}")
        raise HTTPException(status_code=500, detail=f"MCP upload failed: {str(e)}")

    # 2. Call Claude LLM with context
    prompt = f"Analyze the following customer data and provide a summary. Details: {details}"
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    headers_llm = {
        **headers,
        "content-type": "application/json"
    }
    try:
        async with httpx.AsyncClient() as client:
            llm_resp = await client.post(CLAUDE_API_URL, headers=headers_llm, json=payload)
            llm_resp.raise_for_status()
            llm_result = llm_resp.json()
            print(f"[DEBUG] LLM response: {llm_result}")
    except Exception as e:
        print(f"[DEBUG] LLM call error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM call failed: {str(e)}")
    return {"llm_response": llm_result["content"][0]["text"], "context_id": context_id}

@app.post("/api/mcp-upload/")
async def mcp_upload(file: UploadFile = File(...)):
    # Simulate MCP server behavior: accept file and return a mock context_id
    print(f"[DEBUG] MCP upload received file: {file.filename}")
    # Read file content (optional, for logging)
    content = await file.read()
    print(f"[DEBUG] MCP upload file size: {len(content)} bytes")
    # Return a mock context_id
    return {"context_id": "mock_context_id_123"} 