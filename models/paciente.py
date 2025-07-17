from sqlalchemy import Column, String, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db import Base

import enum

class SexoEnum(str, enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    rut = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)

    examenes = relationship("Examen", back_populates="paciente")
