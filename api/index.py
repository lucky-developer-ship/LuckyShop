import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Force SQLite to use /tmp on Vercel (writable directory)
if os.getenv("VERCEL"):
    os.environ["DATABASE_URL"] = "sqlite:////tmp/ecommerce.db"

from app.main import app

