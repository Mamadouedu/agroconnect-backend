from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .models import user    # Pour la table Users
from .models import product
from .db.database import engine, Base
# Imports des routes (Endpoints)
from .api.v1.endpoints import products
from .api.v1.endpoints import auth  # ✅ Importé

# Import des modèles et de la BDD
from .models import user  # Pour que SQLAlchemy crée la table Users

# --- 1. Initialisation de la Base de Données ---
Base.metadata.create_all(bind=engine)

# --- 2. Initialisation de l'API ---
app = FastAPI(
    title="AgroConnect Africa API",
    description="API Backend pour la plateforme AgroConnect (FastAPI + PostgreSQL)",
    version="1.0.0"
)

# --- 3. Configuration CORS (Sécurité) ---
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Enregistrement des Routes ---

# ✅ C'EST LA LIGNE QUI MANQUAIT : On branche l'Authentification
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentification"])

# On branche les Produits
app.include_router(products.router, prefix="/api/v1/products", tags=["Produits"])

# Route de santé (Ping)
@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API AgroConnect Africa 🚀"}

# --- 5. Démarrage ---
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)