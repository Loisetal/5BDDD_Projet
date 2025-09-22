import pytest
from datetime import timedelta
from jose import jwt

from app.core import security


# ⚡ On fixe une clé secrète pour les tests
security.SECRET_KEY = "testsecret"


def test_hash_and_verify_password():
    password = "superpassword"
    hashed = security.hash_password(password)

    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrongpassword", hashed)


def test_create_and_decode_access_token():
    data = {"sub": "1"}
    token = security.create_access_token(data, expire_minutes=5)

    decoded = security.decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "1"


def test_expired_token():
    data = {"sub": "1"}
    # Token expiré directement
    token = security.create_access_token(data, expire_minutes=-1)

    decoded = security.decode_token(token)
    assert decoded is None


def test_token_signature_invalid():
    data = {"sub": "1"}
    token = security.create_access_token(data, expire_minutes=5)

    # On modifie le token pour casser la signature
    parts = token.split(".")
    tampered_token = parts[0] + "." + parts[1] + ".invalidsignature"

    decoded = security.decode_token(tampered_token)
    assert decoded is None
