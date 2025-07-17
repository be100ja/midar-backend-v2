from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from typing import List
import shutil
import os
from db import engine
from models.paciente import Base as PacienteBase
from models.examen import Base as ExamenBase

# Crear tablas automáticamente en la base de datos
PacienteBase.metadata.create_all(bind=engine)
ExamenBase.metadata.create_all(bind=engine)


app = FastAPI()

# Permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bases de datos temporales en memoria
usuarios = {}
pacientes = {}
examenes = {}

# 📍 Registro
@app.post("/registro")
def registrar_usuario(email: str = Form(...), password: str = Form(...), nombre: str = Form(...)):
    if email in usuarios:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user_id = str(uuid4())
    usuarios[email] = {"id": user_id, "email": email, "password": password, "nombre": nombre}
    return {"mensaje": "Usuario creado", "id": user_id}

# 🔐 Login
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    if email not in usuarios or usuarios[email]["password"] != password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {
        "mensaje": "Login exitoso",
        "id": usuarios[email]["id"],
        "nombre": usuarios[email]["nombre"]
    }

# 👤 Crear paciente
@app.post("/pacientes")
def crear_paciente(nombre: str = Form(...), rut: str = Form(...), fecha_nac: str = Form(...), doctor_id: str = Form(...)):
    paciente_id = str(uuid4())
    pacientes[paciente_id] = {
        "id": paciente_id,
        "nombre": nombre,
        "rut": rut,
        "fecha_nac": fecha_nac,
        "doctor_id": doctor_id
    }
    return {"mensaje": "Paciente creado", "id": paciente_id}

# 📂 Obtener pacientes de un doctor
@app.get("/pacientes/{doctor_id}")
def obtener_pacientes(doctor_id: str):
    lista = [p for p in pacientes.values() if p["doctor_id"] == doctor_id]
    return lista

# 🧠 Subir examen de imagen
@app.post("/examenes")
def subir_examen(paciente_id: str = Form(...), tipo: str = Form(...), archivo: UploadFile = File(...)):
    examen_id = str(uuid4())
    folder = "archivos_examenes"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{examen_id}_{archivo.filename}")
    with open(path, "wb") as f:
        shutil.copyfileobj(archivo.file, f)

    examenes[examen_id] = {
        "id": examen_id,
        "paciente_id": paciente_id,
        "tipo": tipo,
        "archivo_path": path
    }
    return {"mensaje": "Examen subido", "id": examen_id}

# 📁 Obtener exámenes por paciente
@app.get("/examenes/{paciente_id}")
def obtener_examenes(paciente_id: str):
    return [e for e in examenes.values() if e["paciente_id"] == paciente_id]
