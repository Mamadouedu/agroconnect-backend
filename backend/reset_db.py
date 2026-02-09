from app.db.database import engine, Base
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
# Importe tous tes modèles ici

print("🗑️ Suppression des tables...")
Base.metadata.drop_all(bind=engine)
print("✅ Tables supprimées !")

print("🏗️ Création des nouvelles tables...")
Base.metadata.create_all(bind=engine)
print("✅ Base de données recréée avec les nouvelles colonnes (phone, image, etc.) !")