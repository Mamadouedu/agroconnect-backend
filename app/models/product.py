from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # Ex: Cacao, Maïs
    variety = Column(String, nullable=True)            # Ex: Mercedes, F1
    
    quantity = Column(Float, nullable=False)           # Ex: 500.0
    unit = Column(String, default="kg")                # Ex: kg, tonnes
    price_per_unit = Column(Float, nullable=True)      # Prix unitaire espéré
    
    location = Column(String, nullable=True)           # Localisation du champ
    description = Column(Text, nullable=True)          # Détails supplémentaires
    
    # Statut de la récolte (planifié, récolté, en_vente, vendu)
    status = Column(String, default="en_stock")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Lien avec l'Agriculteur (User)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

# N'oublie pas d'ajouter la relation inverse dans models/user.py plus tard :
# products = relationship("Product", back_populates="owner")