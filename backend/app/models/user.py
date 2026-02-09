from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(String, default="agriculteur")
    
    # ✅ LES 3 COLONNES DE PROFIL (Location tu l'avais déjà, j'ajoute les autres)
    location = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)  # <-- Manquait
    image_url = Column(String, nullable=True)     # <-- Manquait

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    products = relationship("Product", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")