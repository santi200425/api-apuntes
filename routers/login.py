from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models.usuario import Usuario
from db.cliente import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError

crypt=CryptContext(schemes=["bcrypt"])
router=APIRouter()
oauth=OAuth2PasswordBearer(tokenUrl="login")
DURACION_ACCES_TOKEN=5
ALGORITMO="HS256"
SECRET="mi primer proyecto"


def verificar_token(token:str=Depends(oauth), db:Session=Depends(get_db)):
    try:
        usuario=jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub")
        if usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="credenciales de autenticacion invalidas",
                                headers={"WWW-Authenticate":"Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="credenciales de autenticacion invalidas",
                            headers={"WWW-Authenticate":"Bearer"})
    buscar_usuario=db.query(Usuario).filter(Usuario.id==usuario).first()
    if buscar_usuario!=None:
        return buscar_usuario

def verificar_admin(user:Usuario=Depends(verificar_token)):
    if user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="el usuario no tiene permisos de administrador")
    else:
        return user
    
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    usuario=db.query(Usuario).filter(Usuario.nombre==form.username).first()

    if usuario==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="el nombre de usuario es incorrecto")

    if not crypt.verify(form.password, usuario.contraseña):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    token_acceso={"sub":usuario.id, "exp":datetime.utcnow() + timedelta(minutes=DURACION_ACCES_TOKEN)}

    return {"acces_token":jwt.encode(token_acceso, SECRET, algorithm=ALGORITMO), "token_type":"Bearer"}

@router.get("/usuarios/yo")
async def miUsuario(user:Usuario=Depends(verificar_token)):
    return user