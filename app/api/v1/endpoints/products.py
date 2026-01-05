from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas import product as product_schema
from app.api import deps # On importe notre "Vigile"

router = APIRouter()

# 1. Route pour CRÉER un produit (Sécurisée : il faut être connecté)
@router.post("/", response_model=product_schema.Product)
def create_product(
    product: product_schema.ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user) # Le vigile vérifie le token ici
):
    # On crée le produit et on l'attache automatiquement à l'utilisateur connecté (owner_id)
    new_product = Product(**product.model_dump(), owner_id=current_user.id)
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# 2. Route pour VOIR tous les produits (Public : tout le monde peut voir)
@router.get("/", response_model=List[product_schema.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# 3. Route pour VOIR mes propres produits (Sécurisée)
@router.get("/my-products", response_model=List[product_schema.Product])
def read_my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return current_user.products