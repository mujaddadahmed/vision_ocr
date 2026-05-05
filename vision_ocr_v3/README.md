# Vision-Code Practice — Microservice

A LeetCode-style coding practice section with handwritten code scanning, built with FastAPI + vanilla HTML/CSS/JS.

## Features
- 10 curated coding problems (Easy → Medium)
- Resizable split-panel layout (problem description | code editor)
- Language selector: Python, JavaScript, Java, C++
- **Scan Handwriting** — upload a photo of handwritten code → text appears in editor
- Live console output panel
- Deployable on Railway with zero config

---

## Local Development

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variable
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```
Get an API key at: https://platform.deepseek.com/api_keys

### 3. Run
```bash
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

---

## Deploy on Railway

### Option A — Railway CLI
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Option B — GitHub deploy
1. Push this folder to a GitHub repo
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Select your repo

### Set environment variable on Railway
In your Railway project dashboard:
- Go to **Variables**
- Add: `DEEPSEEK_API_KEY` = `your_api_key_here`

Railway auto-detects Python via Nixpacks and uses `railway.toml` for the start command.

---

## Project Structure
```
vision-code-practice/
├── main.py            # FastAPI app — API routes + static file serving
├── requirements.txt   # Python dependencies
├── railway.toml       # Railway deployment config
├── README.md
└── static/
    └── index.html     # Full frontend (single-file, no build step)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/questions` | List all problems (summary) |
| GET | `/api/questions/{id}` | Full problem detail + starter code |
| POST | `/api/extract-code` | Upload image → returns extracted code |

The `/api/extract-code` endpoint accepts `multipart/form-data` with a single `file` field (image/jpeg, image/png, image/webp).

---

## Adding More Problems
Edit the `QUESTIONS` list in `main.py`. Each question needs:
- `id`, `title`, `difficulty` (Easy/Medium/Hard)
- `tags`, `acceptance`, `description` (HTML allowed)
- `examples` (list of `{input, output, explanation}`)
- `constraints` (list of strings, HTML allowed)
- `starter` (dict with keys: python, javascript, java, cpp)
