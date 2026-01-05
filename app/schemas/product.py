from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Champs communs (utilisés pour créer et lire)
class ProductBase(BaseModel):
    name: str
    variety: Optional[str] = None
    quantity: float
    unit: str = "kg"
    price_per_unit: Optional[float] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: str = "en_stock"

# Ce que l'utilisateur envoie pour CRÉER (Input)
class ProductCreate(ProductBase):
    pass

# Ce que l'API renvoie (Output)
class Product(ProductBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True