import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from core.config import settings

# Salt size & PBKDF2 iterations (OWASP standard)
SALT_BYTES = 16
PBKDF2_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    """Hash a password using standard PBKDF2-HMAC-SHA256 with a secure random salt."""
    salt = secrets.token_bytes(SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    salt_hex = salt.hex()
    hash_hex = dk.hex()
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_hex}${hash_hex}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored PBKDF2 hash using constant-time comparison."""
    try:
        parts = hashed_password.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        expected_hash = bytes.fromhex(parts[3])

        dk = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            iterations,
        )
        return hmac.compare_digest(dk, expected_hash)
    except Exception:
        return False


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    padding = "=" * (4 - (len(data) % 4)) if len(data) % 4 != 0 else ""
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a standard HMAC-SHA256 signed JWT token."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = int(expire.timestamp())
    to_encode["iat"] = int(now.timestamp())

    header = {"alg": "HS256", "typ": "JWT"}
    header_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    payload_bytes = json.dumps(to_encode, separators=(",", ":")).encode("utf-8")

    unsigned_token = f"{_b64_encode(header_bytes)}.{_b64_encode(payload_bytes)}"
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        unsigned_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return f"{unsigned_token}.{_b64_encode(signature)}"


def decode_access_token(token: str) -> Optional[dict]:
    """Verify signature and expiration of an access token, returning payload dict or None."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        unsigned_token = f"{parts[0]}.{parts[1]}"
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            unsigned_token.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        actual_sig = _b64_decode(parts[2])
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_json = _b64_decode(parts[1]).decode("utf-8")
        payload = json.loads(payload_json)

        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > exp:
            return None  # Token expired

        return payload
    except Exception:
        return None
