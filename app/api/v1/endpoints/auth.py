from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ....db.database import get_db
from ....models.user import User as UserModel
from ....schemas import user as user_schema
from ....schemas import token as token_schema # Assure-toi que ce fichier existe (voir étape 2)
from ....core import security

router = APIRouter()

@router.post("/register", response_model=user_schema.User)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Vérification email unique
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà pris")
    
    # Hashage du mot de passe
    hashed_pwd = security.get_password_hash(user.password)
    
    # Création
    new_user = UserModel(
        email=user.email, 
        hashed_password=hashed_pwd, 
        full_name=user.full_name, 
        role=user.role,
        location=user.location # Ajouté car présent dans ton schema
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=token_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. On cherche l'utilisateur
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # 2. Vérification mot de passe
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    # 3. Création du Token (CORRECTION ICI)
    access_token_expires = timedelta(minutes=30) # Durée de vie du token
    token = security.create_access_token(
        data={"sub": user.email}, # C'était ici l'erreur "schemas/user.email"
        expires_delta=access_token_expires
    )
    
    return {"access_token": token, "token_type": "bearer"}