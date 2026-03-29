from sqlalchemy import Column, String, CHAR, ForeignKey, Text,DateTime, func
from db.cliente import base
from sqlalchemy.orm import relationship
import uuid

class Apunte(base):
    __tablename__="apunte"

    id=Column(CHAR(36), primary_key= True, default=lambda:str(uuid.uuid4()))
    titulo=Column(String(100))
    id_materia=Column(CHAR(36), ForeignKey("materia.id"))
    descripcion=Column(Text)
    archivo_url=Column(String(255))
    fecha_creacion=Column(DateTime, server_default=func.now())

    materia=relationship("Materia", back_populates="apuntes")