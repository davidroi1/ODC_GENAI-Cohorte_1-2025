from fastapi import FastAPI, Depends, HTTPException, requests
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import SessionLocal, engine


app = FastAPI()


# Crée les tables
models.Base.metadata.create_all(bind=engine)


# Dépendance DB (inchangée)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_default():
    return "Welcome"


# Routes pour utiliser CRUD
@app.post("/clients/", response_model=schemas.Client)
async def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_client(db=db, client=client)


@app.put("/clients/{client_id}", response_model=schemas.Client)
async def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return crud.update_client(db=db, db_client=db_client, client=client)


@app.delete("/clients/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return crud.delete_client(db=db, db_client=db_client)


@app.get("/clients/{client_id}", response_model=schemas.Client)
async def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return db_client


# Route pour les operations crud sur le produits
# ----------------------------------------------------------------------------------------------------------------------
@app.post("/produit/", response_model=schemas.Produit)
async def create_produit(produit: schemas.ProduitCreate, db: Session = Depends(get_db)):
    return crud.create_produit(db=db, produit=produit)


@app.put("/produit/{produit_id}", response_model=schemas.Produit)
async def update_produit(produit_id: int, produit: schemas.ProduitUpdate, db:Session = Depends(get_db)):
    db_produit = crud.get_produit(db=db, produit_id=produit_id)
    if db_produit is None:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé")
    return crud.update_produit(db=db, db_produit=db_produit, produit=produit)


@app.delete("/produit/{produit_id}")
async def delete_produit(produit_id: int, db: Session = Depends(get_db)):
    produit = crud.get_produit(db=db, produit_id=produit_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé")
    return crud.delete_produit(db=db, produit=produit)


@app.get("/produit/{produit_id}", response_model=schemas.Produit)
async def read_produit(produit_id: int, db: Session = Depends(get_db)):
    db_produit = crud.get_produit(db=db, produit_id=produit_id)
    if db_produit is None:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé")
    return db_produit


# Route pour les operations crud sur le produits
# ----------------------------------------------------------------------------------------------------------------------
@app.post("/commandes/", response_model=schemas.Command)
async def create_commande(commande: schemas.CommandCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client(db=db, client_id=models.Client.id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    # Vérifie que tous les produits existent
    for ligne in commande.command_lines:
        if not crud.get_product(db, ligne.produit_id):
            raise HTTPException(status_code=404, detail=f"Produit {ligne.produit_id} non trouvé")
    
    return crud.create_commande(db=db, commande=commande)