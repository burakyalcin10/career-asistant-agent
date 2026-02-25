# Career Assistant AI Agent 🤖

An AI-powered career assistant that communicates with potential employers on behalf of **Burak Yalçın**. Built with Python, FastAPI, and Google Gemini API.

## Features

- 🤖 **Career Agent**: Generates professional responses using Google Gemini AI with CV context
- 📊 **Response Evaluator**: LLM-as-a-Judge scoring on tone, clarity, completeness, safety, relevance
- 🔄 **Auto-Revision**: Automatically revises responses that score below 7/10 (up to 3 times)
- ⚠️ **Unknown Question Detection**: Hybrid keyword + LLM confidence scoring for salary, legal, and out-of-domain questions
- 📧 **Email Notifications**: Gmail SMTP alerts for new messages, approved responses, and unknown questions
- 💾 **Conversation Memory**: Full history tracking with API endpoint
- 🎨 **Modern Web UI**: Chat interface with evaluation visualization and test cases

## Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=your_email@gmail.com
```

### 3. Run the Server
```bash
cd backend
python main.py
```

### 4. Open in Browser
Navigate to `http://localhost:8000`

## Architecture

```
Frontend (HTML/CSS/JS) ──► FastAPI Backend
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              Career Agent  Evaluator  Unknown Detector
              (Gemini LLM)  (LLM-Judge) (Hybrid KW+LLM)
                    │         │          │
                    └─────────┼──────────┘
                              ▼
                    Google Gemini API
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
                CV Context  Notification  Memory
                (Static)    (Gmail SMTP)  (In-Memory)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/message` | Process employer message |
| GET | `/api/history` | Conversation history |
| GET | `/api/logs` | Agent logs |
| GET | `/api/health` | Health check |

## Test Cases

Use the built-in "Quick Tests" buttons in the UI or run:
```bash
cd tests
python test_cases.py
```

## Project Structure
```
assignment01/
├── backend/
│   ├── main.py              # FastAPI app + agent loop
│   ├── career_agent.py      # Primary Career Agent (Gemini)
│   ├── evaluator_agent.py   # Response Evaluator (LLM-as-Judge)
│   ├── unknown_detector.py  # Unknown Question Detection
│   ├── notification.py      # Email Notification Tool
│   ├── cv_context.py        # CV/Profile Context
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   └── requirements.txt     # Dependencies
├── frontend/
│   ├── index.html           # Chat UI
│   ├── style.css            # Dark theme styling
│   └── app.js               # Frontend logic
├── tests/
│   └── test_cases.py        # 3 test scenarios
├── docs/
│   ├── architecture.md      # Architecture documentation
│   └── report.md            # Assignment report
├── info/
│   ├── cv.md                # CV content
│   └── portfolio.md         # Portfolio content
├── .env                     # Environment variables
└── README.md
```

## Author
**Burak Yalçın** - Computer Engineering, Akdeniz University
