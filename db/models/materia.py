from sqlalchemy import Column, String, DateTime, func, CHAR,ForeignKey, Text
from sqlalchemy.orm import relationship
from db.cliente import base
import uuid

class Materia(base):
    __tablename__="materia"

    id=Column(CHAR(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    nombre=Column(String(100),nullable=False)
    id_usuario=Column(CHAR(36), ForeignKey("usuario.id"))
    descripcion=Column(Text,nullable=True)
    fecha_creacion=Column(DateTime, server_default=func.now())

    usuario=relationship("Usuario", back_populates="materia")
    apuntes=relationship("Apunte", back_populates="materia")
