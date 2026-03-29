from fastapi import APIRouter, HTTPException, status, Depends
from db.cliente import get_db
from sqlalchemy.orm import Session
from db.schemas.materia import Materia_response

router=APIRouter()

@router.get("/materias", response_model=list[])
async def all_materias(db:Session=Depends(get_db)):