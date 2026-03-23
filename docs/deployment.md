
## `docs/deployment.md`

```md
# Deployment

## Local development

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (optional but recommended)
- Git

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
