# Configuration SQLAlchemy ici
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de connexion (pour le dev local)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mamsagro@localhost/agroconnect_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# C'est cette fonction que Python ne trouvait pas !
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()