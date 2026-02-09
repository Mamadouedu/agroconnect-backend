from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
import shutil
import os
import uuid

from app.db.database import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.api import deps

router = APIRouter()

UPLOAD_DIRECTORY = "static/images"

# 1. Lire mon profil
@router.get("/me", response_model=user_schema.User)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user

# 2. Mettre à jour mon profil (Photo + Infos)
@router.put("/me", response_model=user_schema.User)
def update_user_me(
    full_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Gestion de l'image
    if image:
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        file_extension = image.filename.split(".")[-1]
        unique_filename = f"avatar_{current_user.id}_{uuid.uuid4()}.{file_extension}"
        file_path = f"{UPLOAD_DIRECTORY}/{unique_filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        current_user.image_url = f"/static/images/{unique_filename}"

    # Mise à jour des textes
    if full_name:
        current_user.full_name = full_name
    if email:
        current_user.email = email
    if phone_number:
        current_user.phone_number = phone_number
    if location:
        current_user.location = location

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user