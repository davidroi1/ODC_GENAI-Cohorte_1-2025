from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Command(BaseModel):
    demande: str


@dataclass
class Instruction(BaseModel):
    instruction: str