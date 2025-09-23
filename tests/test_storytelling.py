from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_library_story():
    # Créer un utilisateur via l'enregistrement
    user_data = {
        "name": "Utilisateur Test",
        "email": f"user_{uuid.uuid4().hex}@test.com",
        "password": "secret",
        "phone": "0123456789"
    }
    response = client.post("/auth/enregistrement", json=user_data)
    assert response.status_code == 201
    user = response.json()
    user_id = user["id"]

    # Récupérer le token pour les requêtes authentifiées
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    response = client.post("/auth/connexion", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Créer un livre
    book_data = {"title": "Livre Test", "author": "Auteur Test", "genre": "Roman"}
    response = client.post("/book/", json=book_data, headers=headers)
    assert response.status_code == 201
    book_id = response.json()["id"]

    # L'utilisateur emprunte le livre
    loan_data = {"user_id": user_id, "book_id": book_id}
    response = client.post("/loan/", json=loan_data, headers=headers)
    assert response.status_code == 201
    loan_id = response.json()["id"]

    # Vérifier que le livre est maintenant indisponible
    response = client.get(f"/book/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["available"] is False

    # L'utilisateur rend le livre → **PUT au lieu de POST**
    response = client.put(f"/loan/{loan_id}/return", headers=headers)
    assert response.status_code == 200

    # Vérifier que le livre est de nouveau disponible
    response = client.get(f"/book/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["available"] is True
