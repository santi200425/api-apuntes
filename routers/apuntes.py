from fastapi import APIRouter, Depends, HTTPException, status
from .login import verificar_token, verificar_admin
from sqlalchemy.orm import Session
from db.models.apuntes import Apunte
from db.models.usuario import Usuario
from db.models.materia import Materia
from db.schemas.apunte import Apunte_nuevo, Apunte_response, Apunte_update
from db.cliente import get_db


router=APIRouter()

@router.get("/materias/apuntes", response_model=list[Apunte_response])
async def all_apuntes(user:Usuario=Depends(verificar_admin), db:Session=Depends(get_db)):
    lista_apuntes=db.query(Apunte).all()
    return lista_apuntes

@router.get("/mis_materias/mis_apuntes", response_model=list[Apunte_response])
async def apuntes_all(user:Usuario=Depends(verificar_token), db:Session=Depends(get_db)):
    lista_materias=db.query(Materia).filter(Materia.id_usuario==user.id).all()

    lista_apuntes=[]
    for mat in lista_materias:
        lista=db.query(Apunte).filter(Apunte.id_materia==mat.id).all()
        for x in lista:
            new_apunte=Apunte_response(id=x.id, titulo=x.titulo, id_materia=x.id_materia, descripcion=x.descripcion, archivo_url=x.archivo_url, fecha_creacion=x.fecha_creacion)
            lista_apuntes.append(new_apunte)

    if len(lista_apuntes)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no hay apuntes registrados")
    
    return lista_apuntes

@router.get("/mis_materias/{id}/apuntes", response_model=list[Apunte_response])
async def apuntes_por_id(id:str, user:Usuario=Depends(verificar_token), db:Session=Depends(get_db)):
    buscar_materia=db.query(Materia).filter(Materia.id==id).first()

    if buscar_materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="la materia no se encuentra registrada")
    
    if buscar_materia.id_usuario != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no autorisado para ver los apuntes de esta materia")
    lista_apuntes=db.query(Apunte).filter(Apunte.id_materia==id).all()
    
    return lista_apuntes


@router.post("/materias/{idMateria}/nuevo_apunte")
async def registrar_apunte(idMateria:str, apunte:Apunte_nuevo, db:Session=Depends(get_db), user:Usuario=Depends(verificar_token)):
    lista_apuntes=db.query(Apunte).filter(Apunte.id_materia==idMateria).all()

    for x in lista_apuntes:
        if x.titulo == apunte.titulo:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="ya existe un apunte con ese titulo")
        elif x.archivo_url == apunte.archivo_url:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="ya existe ese apunte")
        
    nuevo_apunte=Apunte(titulo=apunte.titulo, id_materia=idMateria, descripcion=apunte.descripcion, archivo_url=apunte.archivo_url)
    db.add(nuevo_apunte)
    db.commit()
    db.refresh(nuevo_apunte)

    return {"detail":"apunte registrado correctamente"}
    

@router.put("/materias/{id_materia}/actualizar_apunte/{id}")
async def act_apunte(id:str, id_materia:str, apunte:Apunte_update, user:Usuario=Depends(verificar_token), db:Session=Depends(get_db)):
    buscar_materia=db.query(Materia).filter(Materia.id_usuario==user.id).first()
    if buscar_materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="la materia no se encuentra registrada")
    
    buscar_apunte=db.query(Apunte).filter(Apunte.id==id).first()
    if buscar_apunte is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El apunte no se encuentra registrada")
    
    if apunte.titulo != None:
        buscar_apunte.titulo=apunte.titulo
    if apunte.descripcion != None:
        buscar_apunte.descripcion=apunte.descripcion
    if apunte.archivo_url != None:
        buscar_apunte.archivo_url=apunte.archivo_url

    db.commit()
    db.refresh(buscar_apunte)
    return {"detail": "apunte actualizado"}

@router.delete("/materias/apuntes/borrar_apunte/{id}")
async def borrar_apunte(id:str, user:Usuario=Depends(verificar_token), db:Session=Depends(get_db)):
    buscar_apunte=db.query(Apunte).filter(Apunte.id == id).first()
    if buscar_apunte is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="apunte no encontrado")
    materia_asociado=db.query(Materia).filter(Materia.id == buscar_apunte.id_materia).first()
    usuario_asociado=db.query(Usuario).filter(Usuario.id == materia_asociado.id_usuario).first()
    if usuario_asociado.id != user.id or buscar_apunte is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="apunte no encontrado")
    
    db.delete(buscar_apunte)
    db.commit()
    return {"detail":"apunte borrado"}