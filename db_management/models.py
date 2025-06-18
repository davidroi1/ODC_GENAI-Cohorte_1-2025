from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from typing import List, Optional


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    pass


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, default=None)
    name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(100))
    tel: Mapped[Optional[str]] = mapped_column(String(15))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.now, default=None
    )
    
    commands: Mapped[List["Command"]] = relationship(
        back_populates="client", 
        cascade="all, delete-orphan",
        default_factory=list,
    )

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, default=None)
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50))
    price: Mapped[float]
    stock: Mapped[int]
    
    command_lines: Mapped[List["CommandLine"]] = relationship(
        back_populates="product", 
        cascade="all, delete-orphan",
        default_factory=list
    )


class Command(Base):
    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, default=None)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), default=None)
    client: Mapped["Client"] = relationship(back_populates="commands", default=None)
    
    command_lines: Mapped[List["CommandLine"]] = relationship(
        back_populates="command", 
        default_factory=list,
        cascade="all, delete-orphan"
    )

class CommandLine(Base):
    __tablename__ = "command_line"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, default=None)
    command_id: Mapped[int] = mapped_column(ForeignKey("commands.id"))  # Renommé pour cohérence
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))  # Renommé pour cohérence
    quantity: Mapped[int]  # Renommé pour cohérence
    unit_price: Mapped[float]  # Renommé pour cohérence

    command: Mapped["Command"] = relationship(back_populates="command_lines")
    product: Mapped["Product"] = relationship(back_populates="command_lines")