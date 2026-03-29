from pydantic import BaseModel
from datetime import datetime

class Apunte_nuevo(BaseModel):
    titulo:str
    descripcion: str | None=None
    archivo_url:str

class Apunte_response(BaseModel):
    id:str
    titulo:str
    id_materia:str
    descripcion:str
    archivo_url:str | None=None
    fecha_creacion:datetime

    class Config:   # 👈 con C mayúscula
        from_attributes = True

class Apunte_update(BaseModel):
    titulo:str | None=None
    descripcion: str | None=None
    archivo_url:str | None=None
