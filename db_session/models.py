from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from typing import List


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    pass


class Client(Base):
    __tablename__ = 'clients'

    _id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str|None] = mapped_column(default=None)
    email: Mapped[str]
    tel: Mapped[str] = mapped_column(String(15))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.now, default=None
    )
    
    addresses: Mapped[List["Command"] | None] = relationship(
        back_populates="clients", cascade="all, delete-orphan", default=None
    )


class Product(Base):
    __tablename__ = 'products'

    _id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True, default=None)
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50))
    price: Mapped[float]
    stock: Mapped[int]
    
    command_lines: Mapped[list["CommandLine"]] = relationship(back_populates="product", default=None)


class Command(Base):
    __tablename__ = "commands"

    _id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True, default=None)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients._id"), default=None)
    client: Mapped["Client"] = relationship(back_populates="command", default=None)
    
    command_lines: Mapped[list["CommandLine"]] = relationship(back_populates="command", default=None)



class CommandLine(Base):
    __tablename__ = "command_line"

    _id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True, default=None)
    id_command: Mapped[int] = mapped_column(ForeignKey("command._id"))
    id_produit: Mapped[int] = mapped_column(ForeignKey("product._id"))
    quantite: Mapped[int]
    prix_unitaire: Mapped[float]

    commande = relationship("Commande", back_populates="lignes_commandes")
    produit = relationship("Produit", back_populates="lignes_commandes")