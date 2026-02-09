from passlib.context import CryptContext

# On configure l'algorithme de hachage (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Transforme un mot de passe en clair en hash sécurisé."""
    return pwd_context.hash(password)