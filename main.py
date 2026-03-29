from fastapi import FastAPI, Depends
from routers import login, usuarios, materias, apuntes
from db.cliente import get_db, SessionLocal
from sqlalchemy.orm import Session
from db.models.usuario import Usuario
from passlib.context import CryptContext

app=FastAPI()
crypt=CryptContext(schemes=["bcrypt"])

app.include_router(login.router)
app.include_router(usuarios.router)
app.include_router(materias.router)
app.include_router(apuntes.router)

def crear_primer_admin():
    db=SessionLocal()
    admin_existente=db.query(Usuario).filter(Usuario.rol=="admin").first()

    if admin_existente == None:
        admin=Usuario(
            nombre="ana",
            email="ana@gmail.com",
            contraseña=crypt.hash("admin123"),
            rol="admin"
        )

        db.add(admin)
        db.commit()
    
    
    db.close()

if __name__=="__main__":
    crear_primer_admin()


#http://127.0.0.1:8000
