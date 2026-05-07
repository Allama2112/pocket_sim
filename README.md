# Pokemon TCG Pocket Simulator

Work in progress 👍

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# OR source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
