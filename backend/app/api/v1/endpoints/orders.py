from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas import order as order_schema
from app.api import deps

router = APIRouter()

# 1. Passer une commande
@router.post("/", response_model=order_schema.Order)
def create_order(
    order: order_schema.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # a. Trouver le produit
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # b. Vérifier le stock
    if product.quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

    # c. Calculer le prix total
    price = product.price_per_unit if product.price_per_unit else 0
    total_price = price * order.quantity

    # d. Créer la commande
    new_order = Order(
        buyer_id=current_user.id,
        product_id=order.product_id,
        quantity_ordered=order.quantity,
        total_price=total_price,
        status="CONFIRMED"
    )

    # e. Mettre à jour le stock
    product.quantity -= order.quantity

    # f. Sauvegarder
    db.add(new_order)
    db.add(product)
    db.commit()
    db.refresh(new_order)
    
    return new_order

# 2. Voir MES achats
@router.get("/my-orders", response_model=List[order_schema.Order])
def read_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return current_user.orders

# 3. Voir MES ventes (côté agriculteur)
@router.get("/my-sales", response_model=List[order_schema.Order])
def read_my_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Trouve les commandes dont le produit appartient à l'utilisateur connecté
    sales = db.query(Order).join(Product).filter(Product.owner_id == current_user.id).all()
    return sales