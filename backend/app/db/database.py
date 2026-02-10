import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. RÉCUPÉRATION INTELLIGENTE DE L'URL
# Si on est sur Render, os.getenv("DATABASE_URL") trouvera le lien.
# Si on est sur ton PC, il ne trouvera rien et utilisera le lien par défaut (localhost).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Mamsagro@localhost/agroconnect_db")

# 2. CORRECTION POUR RENDER
# Render donne parfois des URL commençant par "postgres://", mais SQLAlchemy préfère "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. CRÉATION DU MOTEUR
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 4. FONCTION D'ACCÈS À LA DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()