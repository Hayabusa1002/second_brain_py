# app/main.py
from app.db.session import SessionLocal
from app.models.user import User

def test_connection():
    db = SessionLocal()
    try:
        user = User(name="luis daniel", email="ldfg1002@gmail.com")
        db.add(user)
        db.commit()
        print("Usuario creado")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()