from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .product import Product  # On importe le schéma Product pour l'afficher

# Ce qu'on envoie pour commander (Input)
class OrderCreate(BaseModel):
    product_id: int
    quantity: float

# Ce que l'API renvoie (Output - La facture)
class Order(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    quantity_ordered: float
    total_price: float
    status: str
    created_at: datetime
    
    # Optionnel : On inclut les détails du produit
    product: Optional[Product] = None

    class Config:
        from_attributes = True