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
MCP_UPLOAD_URL = os.getenv("MCP_UPLOAD_URL")

# File upload configuration for Cloudflare Worker
# Your worker only handles file uploads and returns context_id

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
    """
    Analyze customer campaign data using Claude API with actual file content.
    
    This approach:
    1. Reads the uploaded file content locally
    2. Uploads file to Cloudflare Worker for backup/storage (gets context_id)
    3. Sends the actual file content to Claude for analysis
    
    This ensures Claude has access to the real data for accurate analysis.
    """
    # Read file content first
    file_content = await file.read()
    file_text = file_content.decode('utf-8')
    
    # Reset file pointer for the upload to Cloudflare Worker
    await file.seek(0)
    
    # 1. Upload CSV to Cloudflare Worker for storage/backup
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    files = {"file": (file.filename, file_content, file.content_type or "text/csv")}
    try:
        async with httpx.AsyncClient() as client:
            mcp_resp = await client.post(MCP_UPLOAD_URL, files=files)
            mcp_resp.raise_for_status()
            mcp_data = mcp_resp.json()
            context_id = mcp_data["context_id"]
            print(f"[DEBUG] Cloudflare Worker upload response: {mcp_data}")
            print(f"[DEBUG] Received context_id: {context_id}")
    except Exception as e:
        print(f"[DEBUG] Cloudflare Worker upload error: {e}")
        # Continue with analysis even if backup upload fails
        context_id = f"local_{int(datetime.utcnow().timestamp())}"
        print(f"[DEBUG] Using local context_id: {context_id}")

    # 2. Prepare data preview for Claude (limit size to avoid token limits)
    if len(file_text) > 10000:  # If file is very large, truncate for preview
        data_preview = file_text[:10000] + "\n\n[... file truncated for analysis ...]"
        file_size_note = f"Note: File is {len(file_text)} characters. Showing first 10,000 characters."
    else:
        data_preview = file_text
        file_size_note = f"Complete file content ({len(file_text)} characters):"

    # 3. Call Claude API with actual file content
    prompt = f"""Please analyze the following customer campaign data:

{file_size_note}

```csv
{data_preview}
```

Additional context: {details}

Please provide a comprehensive analysis including:
- Customer demographics and segmentation patterns
- Key behavioral trends and insights from the data
- Campaign performance indicators visible in the data
- Specific data-driven recommendations for optimization
- Risk factors and growth opportunities based on the actual data patterns
- Summary statistics and key metrics from the dataset

Focus on actionable insights derived directly from the data provided above.
"""
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",  # Latest Claude model
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "system": "You are an expert data analyst specializing in customer campaign analysis. Analyze the provided CSV data thoroughly and provide specific, data-driven insights based on the actual content shown."
    }
    
    headers_llm = {
        **headers,
        "content-type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            llm_resp = await client.post(CLAUDE_API_URL, headers=headers_llm, json=payload)
            llm_resp.raise_for_status()
            llm_result = llm_resp.json()
            print(f"[DEBUG] Claude API response: {llm_result}")
            
            # Extract the response content
            if "content" in llm_result and len(llm_result["content"]) > 0:
                response_text = llm_result["content"][0]["text"]
            else:
                response_text = "Analysis completed but no content returned."
                
    except httpx.HTTPStatusError as e:
        print(f"[DEBUG] Claude API HTTP error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Claude API error: {e.response.status_code}")
    except Exception as e:
        print(f"[DEBUG] Claude API call error: {e}")
        raise HTTPException(status_code=500, detail=f"Claude API call failed: {str(e)}")
    
    return {
        "llm_response": response_text, 
        "context_id": context_id,
        "file_size": len(file_text),
        "file_name": file.filename,
        "upload_url": MCP_UPLOAD_URL,
        "status": "success"
    }

@app.post("/api/mcp-upload/")
async def mcp_upload(file: UploadFile = File(...)):
    """Proxy file upload to Cloudflare Worker MCP server and return context_id"""
    files = {"file": (file.filename, await file.read(), file.content_type or "text/csv")}
    try:
        async with httpx.AsyncClient() as client:
            mcp_resp = await client.post(MCP_UPLOAD_URL, files=files)
            mcp_resp.raise_for_status()
            mcp_data = mcp_resp.json()
            context_id = mcp_data["context_id"]
            print(f"[DEBUG] MCP proxy upload response: {mcp_data}")
            print(f"[DEBUG] Received context_id from MCP: {context_id}")
            return {"context_id": context_id, "status": "success"}
    except Exception as e:
        print(f"[DEBUG] MCP proxy upload error: {e}")
        raise HTTPException(status_code=500, detail=f"MCP proxy upload failed: {str(e)}")

@app.get("/api/upload/health")
async def upload_health_check():
    """Check health of Cloudflare Worker file upload service"""
    try:
        # Test connection to Cloudflare Worker upload endpoint
        async with httpx.AsyncClient() as client:
            # Try a simple HEAD request to check if upload endpoint is accessible
            response = await client.head(MCP_UPLOAD_URL, timeout=10.0)
            worker_status = "healthy" if response.status_code in [200, 405] else "unhealthy"  # 405 = Method Not Allowed is ok for HEAD
        
        return {
            "status": "healthy",
            "upload_url": MCP_UPLOAD_URL,
            "cloudflare_worker_status": worker_status,
            "claude_api_configured": bool(CLAUDE_API_KEY),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "upload_url": MCP_UPLOAD_URL,
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/api/upload/config")
async def get_upload_config():
    """Get current upload configuration (without sensitive data)"""
    return {
        "upload_url": MCP_UPLOAD_URL,
        "supported_formats": ["csv", "text/csv"],
        "worker_type": "cloudflare",
        "functionality": "file_upload_only"
    }