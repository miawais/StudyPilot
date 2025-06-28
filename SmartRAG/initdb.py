import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.db.database import Base, engine
from app.db.models import ChatLog


Base.metadata.create_all(bind=engine)

print("✅ Database initialized! Table 'chat_logs' created.")
