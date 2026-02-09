from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # Qui achète ? (L'acheteur)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    
    # Quoi ? (Le produit)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Combien ?
    quantity_ordered = Column(Float, nullable=False) # Ex: 50kg
    total_price = Column(Float, nullable=False)      # Ex: 50 * 5 = 250
    
    # Statut de la commande (PENDING, CONFIRMED, DELIVERED, CANCELLED)
    status = Column(String, default="PENDING")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations (Pour pouvoir faire order.buyer.full_name ou order.product.name)
    buyer = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")