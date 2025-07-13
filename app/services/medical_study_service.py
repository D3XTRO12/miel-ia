from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..infrastructure.db.models.medical_study import MedicalStudy
from ..infrastructure.db.models.user import User
from fastapi import HTTPException, logger, status
from typing import List

from ..infrastructure.repositories.medical_study_repo import MedicalStudyRepo
from ..infrastructure.repositories.user_repo import UserRepo
from ..infrastructure.db.DTOs.medical_study_dto import MedicalStudyCreateDTO, MedicalStudyUpdateDTO

class MedicalStudyService:
    def __init__(self, medical_study_repo: MedicalStudyRepo, user_repo: UserRepo):
        self.__medical_study_repo = medical_study_repo
        self.__user_repo = user_repo

    def create_study(self, db: Session, study_data: MedicalStudyCreateDTO):
        # 1. Validar que el código de acceso no exista
        if self.__medical_study_repo.get_by_access_code(db, access_code=study_data.access_code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Access code already exists."
            )

        doctor = self.__user_repo.get(db, id=study_data.doctor_id)

        if not doctor or "DOCTOR" not in [role.name for role in doctor.roles]:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Doctor ID or user is not a doctor.")
        
        patient = self.__user_repo.get(db, id=study_data.patient_id)
        if not patient or "PATIENT" not in [role.name for role in patient.roles]:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Patient ID or user is not a patient.")

        if study_data.technician_id:
            technician = self.__user_repo.get(db, id=study_data.technician_id)
            if not technician:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Technician ID.")

        # 3. Si todo es válido, crear el estudio
        study = self.__medical_study_repo.create(db, obj_in=study_data.model_dump())
        return study

    def get_study_by_id(self, db: Session, study_id: int):
        study = self.__medical_study_repo.get(db, id=study_id)
        if not study:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical study not found.")
        return study
    
    def get_by_patient_dni(self, db: Session, *, dni: str, access_code: str) -> List[MedicalStudy]:
        """
        Obtiene estudios por DNI del paciente con validación de código de acceso.
        """
        # Validaciones de negocio
        if not dni or not access_code:
            raise ValueError("DNI y código de acceso son requeridos")
        
        # Formatear/limpiar DNI si es necesario
        dni = dni.strip().replace("-", "").replace(".", "")
        
        # Llamar al repositorio
        studies = self.__medical_study_repo.get_by_patient_dni_and_access_code(db, dni, access_code)

        if not studies:
            # Log de seguridad: intento de acceso con credenciales inválidas
            logger.warning(f"Intento de acceso con DNI {dni} y código inválido")
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron estudios o credenciales inválidas"
            )
        
        return studies
    def get_by_patient_name(self, db: Session, *, name: str) -> List[MedicalStudy]:
        """
        Busca estudios por nombre o apellido del paciente.
        Es insensible a mayúsculas/minúsculas.
        """
        search_term = f"%{name}%"
        return (
            db.query(self.model)
            .join(User, self.model.patient_id == User.id)
            .filter(
                or_(
                    User.name.ilike(search_term),
                    User.last_name.ilike(search_term)
                )
            )
            .all()
        )
    
    def get_all_studies(self, db: Session) -> List:
        studies = self.__medical_study_repo.get_all(db)
        return studies
    
    def delete_study(self, db: Session, study_id: int):
        """
        Verifica que un estudio exista y luego lo elimina.
        """
        # Reutilizamos el método get_study para manejar el caso de que no exista (error 404)
        study_to_delete = self.get_study_by_id(db, study_id=study_id)
        
        # Si existe, llama al repositorio para eliminarlo
        return self.__medical_study_repo.delete(db, id=study_to_delete.id)
    
    def update(self, db: Session, *, study_id: int, study_update: MedicalStudyUpdateDTO):
        """
        Actualiza un estudio médico de forma parcial (PATCH).
        """
        # 1. Reutilizamos get_study_by_id para encontrar el estudio y manejar el error 404 si no existe
        db_study = self.get_study_by_id(db, study_id=study_id)
        
        # 2. Convertimos el DTO a un diccionario, excluyendo los campos que no se enviaron (None)
        #    Esto es crucial para una operación PATCH.
        update_data = study_update.model_dump(exclude_unset=True)

        # 3. (Opcional pero recomendado) Añadir validaciones de negocio aquí si es necesario.
        #    Por ejemplo, si se intenta cambiar el doctor, verificar que el nuevo ID sea válido.
        if "doctor_id" in update_data:
            new_doctor_id = update_data["doctor_id"]
            doctor = self.__user_repo.get(db, id=new_doctor_id)
            if not doctor or "DOCTOR" not in [role.name for role in doctor.roles]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid new Doctor ID: {new_doctor_id}")
        
        # 4. Llamar al repositorio para aplicar los cambios en la base de datos
        return self.__medical_study_repo.update(db, db_obj=db_study, obj_in=update_data)
