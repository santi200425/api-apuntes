from pydantic import BaseModel
from datetime import datetime

class Materia_nueva(BaseModel):
    nombre:str
    descripcion:str | None=None

class Materia_response(BaseModel):
    id:str
    nombre:str
    id_usuario:str
    descripcion: str | None=None
    fecha_creacion: datetime

    class Config:
        from_attributes=True

class Materia_update(Materia_nueva):
    nombre:str | None=None