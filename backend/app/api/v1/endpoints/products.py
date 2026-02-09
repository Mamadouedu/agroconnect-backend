from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_
import shutil
import os
import uuid # Pour générer des noms de fichiers uniques

from app.db.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas import product as product_schema
from app.api import deps

router = APIRouter()

# Dossier où on sauvegarde les images (doit correspondre à ce qu'on a créé à l'étape 1)
UPLOAD_DIRECTORY = "static/images"

# 1. Route pour CRÉER un produit AVEC IMAGE
# Note : On ne peut plus utiliser le schéma Pydantic ProductCreate directement dans les arguments
# quand on utilise UploadFile. On utilise donc Form(...) pour chaque champ.
@router.post("/", response_model=product_schema.Product)
def create_product(
    name: str = Form(...),
    quantity: float = Form(...),
    price_per_unit: Optional[float] = Form(None),
    unit: str = Form("kg"),
    description: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    variety: Optional[str] = Form(None),
    image: UploadFile = File(None), # <-- Le fichier image (optionnel)
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    image_url = None
    
    # Si une image est envoyée
    if image:
        # 1. On s'assure que le dossier existe
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        
        # 2. On génère un nom unique pour éviter d'écraser les fichiers (ex: mon_image.jpg devient un-code-unique.jpg)
        file_extension = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"{UPLOAD_DIRECTORY}/{unique_filename}"
        
        # 3. On sauvegarde le fichier sur le disque
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # 4. On définit l'URL publique de l'image
        image_url = f"/static/images/{unique_filename}"

    # On crée le produit dans la BDD avec les infos du formulaire
    new_product = Product(
        name=name,
        quantity=quantity,
        price_per_unit=price_per_unit,
        unit=unit,
        description=description,
        location=location,
        variety=variety,
        image_url=image_url, # On ajoute l'URL ici
        owner_id=current_user.id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# ... (Les routes GET read_products et read_my_products ne changent pas, garde-les en dessous) ...
@router.get("/", response_model=List[product_schema.Product])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = Query(None, description="Recherche par nom ou description"),
    location: Optional[str] = Query(None, description="Filtrer par ville"),
    category: Optional[str] = Query(None, description="Filtrer par variété/catégorie"),
    min_price: Optional[float] = Query(None, description="Prix minimum"),
    max_price: Optional[float] = Query(None, description="Prix maximum"),
    db: Session = Depends(get_db)
):
    # 1. On commence avec tous les produits
    query = db.query(Product)
    
    # 2. Si l'utilisateur cherche un mot-clé (ex: "Cacao")
    if search:
        # On cherche si le mot est dans le NOM ou la DESCRIPTION
        # ilike veut dire "Insensible à la casse" (Cacao = cacao)
        search_filter = or_(
            Product.name.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # 3. Si l'utilisateur filtre par Ville (ex: "Bouaké")
    if location:
        query = query.filter(Product.location.ilike(f"%{location}%"))
        
    # 4. Si l'utilisateur filtre par Variété
    if category:
        query = query.filter(Product.variety.ilike(f"%{category}%"))

    # 5. Filtre par tranche de prix
    if min_price is not None:
        query = query.filter(Product.price_per_unit >= min_price)
    if max_price is not None:
        query = query.filter(Product.price_per_unit <= max_price)

    # 6. On applique la pagination et on envoie le résultat
    products = query.offset(skip).limit(limit).all()
    return products