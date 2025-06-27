from app.db.database import Base, engine
from app.db.models import ChatLog

Base.metadata.create_all(bind=engine)
