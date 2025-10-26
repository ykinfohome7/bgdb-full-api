from app.core.database import SessionLocal, engine
from app.core.database import Base
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email=="admin@bgdb.eu").first():
            admin = User(email="admin@bgdb.eu", hashed_password=get_password_hash("Admin123!"), is_superuser=True, full_name="BGDB Admin")
            db.add(admin)
            db.commit()
        print("Seed complete.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
