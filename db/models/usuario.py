from sqlalchemy import Column, String, DateTime, func, CHAR
from sqlalchemy.orm import relationship
from db.cliente import base
import uuid

class Usuario(base):
    __tablename__="usuario"

    id=Column(CHAR(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    nombre=Column(String(100),nullable=False)
    email=Column(String(100), nullable=False, unique=True)
    contraseña=Column(String(100),nullable=False)
    fecha_creacion=Column(DateTime, server_default=func.now())
    rol=Column(String(20), default="usuario")

    materia=relationship("Materia", back_populates="usuario")
