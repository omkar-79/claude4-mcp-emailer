# Cloudflare Worker File Upload Integration Guide

## Overview

Your application now correctly integrates with your Cloudflare Worker file upload service. The code has been simplified to match your actual setup - your worker only handles file uploads and storage, not MCP tool execution.

## Key Changes Made

### ❌ **What Was Fixed:**
- Removed invalid `"context": context_id` parameter 
- Removed unnecessary MCP server configuration (your worker doesn't expose MCP tools)
- Updated to latest Claude model (`claude-3-5-sonnet-20241022`)
- Simplified to match your actual worker functionality

### ✅ **What's Now Working:**
- Simple file upload to Cloudflare Worker
- Context ID reference in prompts to Claude
- Enhanced error handling and logging  
- Health check endpoints for upload service

## Environment Variables

Add these to your `.env` file:

```env
# Claude API Configuration
CLAUDE_API_KEY=your_anthropic_api_key_here
CLAUDE_API_URL=https://api.anthropic.com/v1/messages

# Cloudflare Worker Upload Configuration  
MCP_UPLOAD_URL=https://my-mcp-server.omkarbalekundri79.workers.dev/upload
```

## How It Works Now

1. **File Reading**: Your FastAPI backend reads the uploaded file content locally
2. **File Upload**: The file is also uploaded to your Cloudflare Worker for backup/storage
3. **Context ID**: The worker returns a `context_id` for reference
4. **Data Analysis**: The actual file content is sent to Claude in the prompt for real analysis
5. **Response**: Claude provides analysis based on the actual data content

## API Payload Structure

The corrected Claude API call now includes actual file content:

```python
prompt = f"""Please analyze the following customer campaign data:

{file_size_note}

```csv
{data_preview}
```

Additional context: {details}
...
"""

payload = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": prompt}],
    "system": "You are an expert data analyst..."
}
```

Claude now receives the actual CSV data content for real analysis.

## New Endpoints

### Health Check
```
GET /api/upload/health
```
Returns the status of your Cloudflare Worker upload service.

### Configuration
```
GET /api/upload/config  
```
Returns current upload configuration.

## Testing Your Setup

1. **Test the health endpoint:**
   ```bash
   curl http://localhost:8000/api/upload/health
   ```

2. **Upload a test file:**
   ```bash
   curl -X POST -F "file=@test.csv" -F "details=test analysis" \
        http://localhost:8000/api/analyze-campaign/
   ```

3. **Check the logs** for debug information about the upload process.

## Cloudflare Worker Requirements

Your Cloudflare Worker should support:

- File upload endpoint (`/upload`)
- KV storage for uploaded files
- Return `context_id` for uploaded files
- CORS enabled for cross-origin requests

## Troubleshooting

### Common Issues:

1. **Invalid context parameter error** ❌ Fixed
2. **Model not found** ❌ Fixed (updated to latest model)
3. **"Unable to access file with context ID"** ❌ Fixed (now sends actual file content)
4. **Cloudflare Worker not responding**: Check health endpoint
5. **Authorization issues**: Verify API key in environment
6. **File too large**: Files over 10,000 characters are truncated for analysis

### Debug Logs:

The application now provides detailed logging:
- `[DEBUG] Cloudflare Worker MCP response`
- `[DEBUG] Claude API response`
- `[DEBUG] Claude API HTTP error`

## Next Steps

1. **Update your `.env`** with the new variables
2. **Test the integration** using the health check endpoint
3. **Monitor the logs** for any issues
4. **Consider upgrading to Claude 4** when available for even better performance

## Security Notes

- API keys are properly handled through environment variables
- Authorization tokens are passed securely to the MCP server
- Sensitive data is excluded from configuration endpoints

Your Cloudflare Worker MCP integration is now properly configured and should work correctly with the Claude API! 