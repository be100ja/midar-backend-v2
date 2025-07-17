from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db import Base
import enum

class TipoExamenEnum(str, enum.Enum):
    mri = "MRI"
    pet_ct = "PET-CT"
    otro = "Otro"

class Examen(Base):
    __tablename__ = "examenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo = Column(Enum(TipoExamenEnum), nullable=False)
    fecha = Column(Date, nullable=False)
    archivo_imagen = Column(String, nullable=False)  # Ruta del archivo .nii.gz o similar

    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.id"))
    paciente = relationship("Paciente", back_populates="examenes")
