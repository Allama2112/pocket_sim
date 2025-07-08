# Pocket Simulator

A web-based simulator for Pokémon TCG Pocket, allowing deck creation and battles.

## Tech Stack

- **Frontend:** React, Axios, Tailwind CSS  
- **Backend:** FastAPI (Python)  
- **Database:** (To be connected, e.g., Supabase)

## Getting Started

### Prerequisites

- Python 3.10+  
- Node.js and npm  
- (Optional) Virtual environment tool like `venv`

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# OR source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
