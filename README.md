# Email Buddy AI 📧

![Email Buddy Logo](frontend/public/emailbuddylogo.png)

An AI-powered email campaign management system that analyzes customer data and generates personalized marketing emails using Claude AI.

## What It Does

- **CSV Analysis**: Upload customer data CSV files and get AI-powered insights using Claude
- **Customer Selection**: Select specific customers from your data based on customer IDs
- **Personalized Email Generation**: Generate tailored marketing emails for selected customers using their full profile data
- **User Authentication**: Secure login/registration system
- **Campaign Management**: Create and manage multiple email campaigns

## Tech Stack

- **Frontend**: Vue.js 3 with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI**: Claude 3.5 Sonnet API
- **File Storage**: Cloudflare Worker (MCP server)
- **Authentication**: JWT

## Quick Setup

### Prerequisites
- Docker and Docker Compose
- Claude API key
- Cloudflare Worker URL (for file storage)

### Environment Variables
Create `.env` files in both `backend/` and `frontend/` directories:

**Backend (.env):**
```env
CLAUDE_API_KEY=your_claude_api_key
CLAUDE_API_URL=https://api.anthropic.com/v1/messages
MCP_UPLOAD_URL=your_cloudflare_worker_url
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=postgresql://postgres:postgres@db:5432/email_gen
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000/api
```

### Run the Application

1. **Clone the repository:**
```bash
git clone https://github.com/omkar-79/claude4-mcp-emailer.git
cd claude4-mcp-emailer
```

2. **Start with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Database: localhost:5432

### Manual Setup (Alternative)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. **Register/Login** to your account
2. **Upload CSV** with customer data
3. **Analyze** the data with Claude AI
4. **Select Customer ID column** from your CSV
5. **Choose customers** for email generation
6. **Generate personalized emails** using customer profile data

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/token` - User login
- `POST /api/analyze-campaign/` - Analyze CSV data with Claude
- `POST /api/generate-emails/` - Generate personalized emails
- `GET /api/users/me` - Get current user info

## Project Structure

```
├── frontend/          # Vue.js frontend
├── backend/           # FastAPI backend
├── data/             # Sample CSV files
├── uploads/          # File uploads
└── docker-compose.yml
```

## License

MIT License - see LICENSE file for details.

