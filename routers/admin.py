from fastapi import APIRouter, HTTPException, status, Depends
from db.cliente import get_db
from sqlalchemy.orm import Session
from db.schemas.materia import Materia_response
from db.models.materia import Materia
from db.models.usuario import Usuario

router=APIRouter()

@router.get("/materias", response_model=list[Materia_response])
async def all_materias(db:Session=Depends(get_db), user:Usuario=Depends()):
    lista_materias=db.query(Materia).all()
    return lista_materias

@router.get("/usuarios", response_model=list[Usuario])
async def all_usuarios(db:Session=(get_db)):
    lista_usuarios=db.query(Usuario).all()
    return lista_usuarios