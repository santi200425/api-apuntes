from fastapi import APIRouter, HTTPException, status,Depends
from passlib.context import CryptContext
from db.cliente import get_db
from sqlalchemy.orm import Session
from db.models.usuario import Usuario
from db.schemas.usuario import Usuario_nuevo, Usuario_respuesta, Usuario_update
from .login  import verificar_admin

router=APIRouter()
crypt=CryptContext(schemes=["bcrypt"])


@router.get("/usuarios", response_model=list[Usuario_respuesta])
async def all_usuarios(db:Session=Depends(get_db), user:Usuario=Depends(verificar_admin)):
    lista_usuarios=db.query(Usuario).all()
    return lista_usuarios

@router.post("/new_usuario", response_model=Usuario_respuesta)
async def register_usuario(user:Usuario_nuevo, db:Session=Depends(get_db)):
    buscar_usuario=db.query(Usuario).filter(Usuario.nombre==user.nombre).first()
    if buscar_usuario != None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="el usuario ya se encuentra registrado")
    
    contraseña_hash=crypt.hash(user.contraseña)
    nuevo_usuario=Usuario(nombre=user.nombre, email=user.email, contraseña=contraseña_hash)

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/actualizar")
async def actualizar_usuario(user:Usuario_update, db:Session=Depends(get_db)):
    buscar_usuario=db.query(Usuario).filter(user.id==Usuario.id).first()
    if buscar_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario no se encuentra registrado")
    
    if user.nombre!=None:
        buscar_usuario.nombre=user.nombre
    if user.email!=None:
        buscar_usuario.email=user.email
    if user.contraseña!=None:
        buscar_usuario.contraseña=crypt.hash(user.contraseña)

    db.commit()
    db.refresh(buscar_usuario)
    return {"detail":"usuario actualizado"}

@router.delete("/usuarios/{id}")
async def borrar_usuario(id:str, db:Session=Depends(get_db), user:Usuario=Depends(verificar_admin)):
    buscar_usuario=db.query(Usuario).filter(Usuario.id==id).first()
    if buscar_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario no fue encontrado")
    
    db.delete(buscar_usuario)
    db.commit()
    return{"detail":"usuario borrado"}