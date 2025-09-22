from sqlalchemy import text
from app.db.database import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connexion OK :", result.scalar_one())
    except Exception as e:
        print("Erreur connexion :", e)

if __name__ == "__main__":
    test_connection()
