 Contract Intelligence Platform

Upload any legal contract and get:
- **Clause extraction** — identifies and classifies every clause type
- **Loophole detection** — flags vague language and missing protections
- **Obligation extraction** — maps who must do what by when
- **Risk scoring** — 1–10 score with full issue breakdown
- **AI lawyer chat** — ask anything about your contract in plain English

Project structure
lexis-ai/
│
├── frontend/                        ← Everything the user sees
│   ├── index.html                   ← Full single-page app (landing + dashboard + upload + analysis + chat + settings)
│   └── src/
│       ├── styles/
│       │   └── main.css             ← Complete dark theme CSS
│       └── components/
│           ├── demo-data.js         ← Realistic demo contract + pre-built analysis result
│           ├── ai-providers.js      ← All AI API calls: Gemini, Groq, Claude, Demo
│           ├── analysis-engine.js   ← Progress animation + UI population + export
│           └── app.js               ← Navigation, settings, chat, dashboard logic
│
├── backend/                         ← Python API server (optional for frontend-only use)
│   ├── main.py                      ← FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── routers/
│   │   ├── analysis.py              ← POST /api/analyze
│   │   ├── chat.py                  ← POST /api/chat
│   │   ├── contracts.py             ← GET/POST/DELETE /api/contracts
│   │   └── upload.py                ← POST /api/upload (PDF/DOCX/TXT parsing)
│   └── models/
│       └── contract.py              ← SQLAlchemy model (for when you add PostgreSQL)
│
├── docker-compose.yml               ← One command: frontend + backend + database
├── .gitignore
└── README.md

