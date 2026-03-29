from pydantic import BaseModel
from datetime import datetime

class Usuario_nuevo(BaseModel):
    nombre:str
    email:str
    contraseña:str

class Usuario_respuesta(BaseModel):
    id:str
    nombre:str
    email:str
    fecha_creacion:datetime
    rol:str

    class Config:
        from_attributes=True

class Usuario_update(BaseModel):
    id:str
    nombre: str | None=None
    email: str | None=None
    contraseña: str | None=None