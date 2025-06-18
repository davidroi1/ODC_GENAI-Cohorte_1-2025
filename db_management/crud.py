from sqlalchemy.orm import Session
import schemas
import models


# Opérations CRUD pour les Clients
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    client_info = client.model_dump()
    db_client = models.Client(**client_info)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, db_client: models.Client, client: schemas.ClientUpdate):
    client_data = client.model_dump(exclude_unset=True) # exclude_unset=True pour ne pas mettre à jour les champs non fournis
    for key, value in client_data.items():
        setattr(db_client, key, value)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, db_client: models.Client):
    db.delete(db_client)
    db.commit()
    return {"message": "Client supprimé avec succès"}


#------------------------------------------------------------------------------------------------------------------------
# Opérations CRUD pour les Produits
def get_produit(db: Session, produit_id: int):
    return db.query(models.Product).filter(models.Product.id == produit_id).first()


def get_produits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_produit(db: Session, produit: schemas.ProduitCreate):
    produit_info = produit.model_dump()
    db_produit = models.Product(**produit_info)
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit


def update_produit(db: Session, db_produit: schemas.Produit, produit: schemas.ProduitUpdate):
    produit_info = produit.model_dump(exclude_unset=True)
    for key, value in produit_info.items():
        setattr(db_produit, key, value)
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit


def delete_produit(db: Session, produit: schemas.ProduitCreate):
    db.delete(produit)
    db.commit()
    return {"message": "Le produit a bien ete supprimer"}


# Opérations CRUD pour les Commandes
def create_commande(db: Session, commande: schemas.CommandCreate):
    # Crée la commande
    db_commande = models.Command(
        client_id=commande.client_id,
        commentaire=commande.comments
    )
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    
    # Crée les lignes de commande associées
    for line in commande.command_lines:
        db_line = models.CommandLine(
            id_command=db_commande.id,
            id_produit=line.produit_id,
            quantite=line.quantite
        )
        db.add(db_line)
    
    db.commit()
    db.refresh(db_commande)
    return db_commande


def get_commande(db: Session, commande_id: int):
    return db.query(models.Command).filter(models.Command.id == commande_id).first()


def get_commandes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Command).offset(skip).limit(limit).all()