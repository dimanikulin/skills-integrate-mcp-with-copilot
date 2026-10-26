import getpass
import hashlib
import json
import secrets
from pathlib import Path


TEACHER_CREDENTIALS_PATH = Path(__file__).parent / "teachers.json"
PBKDF2_ITERATIONS = 310_000


def main():
    username = input("Teacher username: ").strip()
    password = getpass.getpass("Teacher password: ")
    password_confirmation = getpass.getpass("Confirm password: ")

    if not username or not password:
        raise SystemExit("Username and password are required.")
    if password != password_confirmation:
        raise SystemExit("Passwords do not match.")

    if TEACHER_CREDENTIALS_PATH.exists():
        credentials = json.loads(TEACHER_CREDENTIALS_PATH.read_text())
    else:
        credentials = {"teachers": []}

    teachers = credentials.get("teachers")
    if not isinstance(teachers, list):
        raise SystemExit("Credential file must contain a teachers list.")
    if any(teacher.get("username") == username for teacher in teachers):
        raise SystemExit("That username already exists.")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, PBKDF2_ITERATIONS
    )
    teachers.append({
        "username": username,
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
    })
    TEACHER_CREDENTIALS_PATH.write_text(json.dumps(credentials, indent=2) + "\n")
    print(f"Created teacher account: {username}")


if __name__ == "__main__":
    main()