from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "agriculteur"
    location: Optional[str] = None
    phone_number: Optional[str] = None  # ✅ AJOUTÉ ICI (pour l'affichage par défaut)

class UserCreate(UserBase):
    password: str

# Ce qu'on reçoit pour MODIFIER un profil
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    # L'image sera gérée à part via UploadFile

class User(UserBase):
    id: int
    is_active: bool
    image_url: Optional[str] = None  # L'URL de l'avatar

    # Nouvelle syntaxe Pydantic V2 (Suffisante, pas besoin de class Config en plus)
    model_config = ConfigDict(from_attributes=True)