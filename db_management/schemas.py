from pydantic import BaseModel, EmailStr
from typing import Optional, List, ForwardRef


# ------ Déclaration anticipée pour résoudre les références circulaires ------
CommandRef = ForwardRef('Command')


# -----------------------------------------------------------
# Schéma Produit
class ProduitBase(BaseModel):
    name: str
    category: str


class ProduitCreate(ProduitBase):
    price: float
    stock: int


class ProduitUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class Produit(ProduitBase):
    id: int
    category: str

    class Config:
        from_attributes = True


# -----------------------------------------------------------
# Schéma LigneCommande
class CommandLineBase(BaseModel):
    quantite: int
    prix_unitaire: float


class CommandLineCreate(CommandLineBase):
    produit_id: int  # ID du produit associé


class CommandLineUpdate(BaseModel):
    quantite: Optional[int] = None
    prix_unitaire: Optional[float] = None
    produit_id: Optional[int] = None  # Pour changer le produit associé


class CommandLine(CommandLineBase):
    id: int
    produit: Produit  # Inclut le produit complet

    class Config:
        from_attributes = True


# -----------------------------------------------------------
# Schéma Commande
class CommandBase(BaseModel):
    comments: Optional[str] = None


class CommandCreate(CommandBase):
    command_lines: List[CommandLineCreate]  # Liste des lignes de Command


class CommandUpdate(BaseModel):
    comments: Optional[str] = None


class Command(CommandBase):
    id: int
    client_id: int
    command_lines: List[CommandLine] = []  # Relation avec les lignes

    class Config:
        from_attributes = True

#----------------------------------------------------------------------------------------------------
# Schéma Client
class ClientBase(BaseModel):
    name: str
    first_name: Optional[str]
    email: EmailStr
    tel: Optional[str] = None  # Optionnel


# Schéma pour la création (reçoit les données du client)
class ClientCreate(ClientBase):
    # Peut ajouter des champs spécifiques à la création
    pass


# schema for update client
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[EmailStr] = None
    tel: Optional[str] = None


# Schéma pour la lecture (renvoyé au client)
class Client(ClientBase):
    id: int
    commands: List["Command"] = []  # Relation avec les commandes

    class Config:
        orm_mode = True  # Permet la compatibilité avec SQLAlchemy


# Résolution des références circulaires
Client.model_rebuild()
Command.model_rebuild()