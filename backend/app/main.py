from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
import uvicorn

# --- A. IMPORT DES MODÈLES (Pour la Base de Données) ---
from .db.database import engine, Base
from .models import user     # Singulier
from .models import product  # Singulier
from .models import order    # Singulier (C'est ta ligne 10 actuelle)

# --- B. IMPORT DES ROUTES (Pour les liens URL / Swagger) ---
from .api.v1.endpoints import auth
from .api.v1.endpoints import products
# ✅ C'EST CETTE LIGNE QU'IL TE MANQUAIT (Note le 's' et le dossier endpoints) :
from .api.v1.endpoints import orders 
from .api.v1.endpoints import users # Pour les routes de profil utilisateur (lecture et mise à jour)

# --- C. CRÉATION DES TABLES ---
Base.metadata.create_all(bind=engine)

# --- 2. Initialisation de l'API ---
app = FastAPI(
    title="AgroConnect Africa API",
    description="API Backend pour la plateforme AgroConnect (FastAPI + PostgreSQL)",
    version="1.0.0"
)

# ✅ AJOUTE CE BLOC JUSTE APRÈS LA CRÉATION DE 'app' :
# Cela permet d'accéder aux images via http://localhost:8000/static/images/ton_image.jpg
# Assure-toi que le dossier "static" existe bien à la racine de "backend"
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    print("⚠️ Attention : Le dossier 'static' n'existe pas encore. Créez-le pour activer les images.")

# --- 3. Configuration CORS ---
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
#  2. AJOUTE CETTE LIGNE POUR ACTIVER LES COMMANDES
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Commandes"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Utilisateurs"])
# Route de santé (Ping)
@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API AgroConnect Africa 🚀"}

# --- 5. Démarrage ---
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)