# Reporter AI

Detector de desinformación basado en verificación por afirmaciones.

## Stack
- Frontend: React + Vite
- Backend: FastAPI
- IA: OpenAI Responses API
- Búsqueda web: Tavily

## Arranque local

### Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` con tus claves y ejecuta:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend
En otra terminal:
```bash
cd frontend
npm install
npm run dev
```

No pongas nunca las claves API en el frontend.
