from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.models.materia import Materia
from db.schemas.materia import Materia_nueva, Materia_response, Materia_update
from .login import verificar_token
from db.cliente import get_db
from db.models.usuario import Usuario

router=APIRouter()

@router.get("/materias", response_model=list[Materia_response])
async def mis_materias(user:Usuario=Depends(verificar_token),db:Session=Depends(get_db)):
    materias=db.query(Materia).filter(Materia.id_usuario==user.id).all()

    if materias is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="no hay materias registradas")
    
    return materias

@router.post("/nueva_materia", response_model=Materia_response)
async def registrar_materia(materia:Materia_nueva,user:Usuario=Depends(verificar_token), db:Session=Depends(get_db)):
    nueva_materia=Materia(nombre=materia.nombre, id_usuario=user.id, descripcion=materia.descripcion)
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia

@router.put("/actualizar_materia/{id}")
async def act_materia(id:str, materia:Materia_update, db:Session=Depends(get_db), user:Usuario=Depends(verificar_token)):
    materias_user=db.query(Materia).filter(Materia.id_usuario==user.id).all()
    materia_encontrada:Materia=None
    for buscar_materia in materias_user:
        if buscar_materia.id==id:
            materia_encontrada=buscar_materia
            
    if materia_encontrada is not None:
        if materia.nombre != None:
            materia_encontrada.nombre=materia.nombre
        if materia.descripcion != None:
            materia_encontrada.descripcion=materia.descripcion
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="materia no encontrada")
        
    db.commit()
    db.refresh(materia_encontrada)
    return {"detail":"materia actualizada"}

@router.delete("/eliminar_materia/{id}")
async def delete_materia(id:str, db:Session=Depends(get_db), user:Usuario=Depends(verificar_token)):
    lista_materias=db.query(Materia).filter(Materia.id_usuario==user.id).all()

    for materia in lista_materias:
        if materia.id==id:
            db.delete(materia)
            db.commit()
            return {"detail":"materia borrada"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="materia no encontrada")