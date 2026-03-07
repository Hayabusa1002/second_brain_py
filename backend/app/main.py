# app/main.py
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.user import User

def create_test_user():
    db = SessionLocal()
    try:
        user = User(name="Luis Daniel", email="ldfg1002@gmail.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Usuario creado con ID: {user.id}")
    finally:
        db.close()

def main():
    init_db()
    create_test_user()

if __name__ == "__main__":
    main()