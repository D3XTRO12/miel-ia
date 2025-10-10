from uuid import UUID
from sqlalchemy.orm import Session, joinedload 
from sqlalchemy import or_
from ..infrastructure.db.models.medical_study import MedicalStudy
from ..infrastructure.db.models.user import User
from fastapi import HTTPException, logger, status
from typing import List, Optional

from ..infrastructure.repositories.medical_study_repo import MedicalStudyRepo
from ..infrastructure.repositories.user_repo import UserRepo
from ..infrastructure.db.DTOs.medical_study_dto import MedicalStudyCreateDTO, MedicalStudyUpdateDTO, MedicalStudyResponseDTO


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

        # 2. Validar doctor
        doctor = self.__user_repo.get(db, id=study_data.doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor not found.")
        
        # OBTENER LOS IDs REALES DE ROLES DESDE LA BD
        admin_role_id, doctor_role_id, patient_role_id = self.__get_role_ids_from_db(db)
        
        doctor_role_ids = [str(role.id) for role in doctor.roles]
        doctor_role_names = [role.name for role in doctor.roles]
        
        print(f"Doctor {doctor.id} has role names: {doctor_role_names}")
        print(f"Doctor {doctor.id} has role IDs: {doctor_role_ids}")
        print(f"Expected Doctor role ID: {doctor_role_id}")
        
        # Verificar por ID del rol Doctor
        has_doctor_role = (
            "Doctor" in doctor_role_names or 
            str(doctor_role_id) in doctor_role_ids
        )
        
        if not has_doctor_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"User is not a doctor. User has roles: {doctor_role_names}"
            )
        
        # 3. Validar patient
        patient = self.__user_repo.get(db, id=study_data.patient_id)
        if not patient:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient not found.")
        
        patient_role_ids = [str(role.id) for role in patient.roles]
        patient_role_names = [role.name for role in patient.roles]
        
        print(f"Patient {patient.id} has role names: {patient_role_names}")
        print(f"Expected Patient role ID: {patient_role_id}")
        
        # Verificar por ID del rol Patient
        has_patient_role = (
            "Patient" in patient_role_names or 
            str(patient_role_id) in patient_role_ids
        )
        
        if not has_patient_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"User is not a patient. User has roles: {patient_role_names}"
            )

        # 4. Validar technician (opcional)
        if study_data.technician_id:
            technician = self.__user_repo.get(db, id=study_data.technician_id)
            if not technician:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Technician not found.")

        # 5. Crear el estudio
        try:
            study_dict = study_data.model_dump()
            study = self.__medical_study_repo.create(db, obj_in=study_dict)
            return MedicalStudyResponseDTO.model_validate(study)
        except Exception as e:
            print(f"❌ Error creating study: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating medical study"
            )

    def __get_role_ids_from_db(self, db: Session):
        """
        Obtiene los IDs reales de roles desde la base de datos
        """
        try:
            # Obtener roles desde la BD
            from ..infrastructure.db.models.role import Role
            roles = db.query(Role).all()
            
            role_map = {}
            for role in roles:
                role_map[role.name] = role.id
            
            print("🔍 Role IDs from database:")
            for name, role_id in role_map.items():
                print(f"  {name}: {role_id}")
            
            return (
                role_map.get('Admin'),
                role_map.get('Doctor'), 
                role_map.get('Patient')
            )
        except Exception as e:
            print(f"❌ Error getting roles from DB: {e}")
            # Fallback a los IDs que sabemos que existen
            return (
                UUID("2dedc6ff-999d-4080-bd2b-918e6ce6159d"),  # Admin
                UUID("ac3e3928-fd43-4008-bdf1-13481820930e"),  # Doctor  
                UUID("f84bbfdd-1518-4e1f-9a11-5fc50cdcb3e9")   # Patient
            )

    # ... el resto de tus métodos permanecen igual


    def get_by_id(self, db: Session, study_id: UUID) -> Optional[MedicalStudyResponseDTO]:
        """
        Obtiene un estudio médico por ID y lo convierte a DTO.
        """
        # Cargar el estudio con todas las relaciones
        study = db.query(MedicalStudy).options(
            joinedload(MedicalStudy.patient),
            joinedload(MedicalStudy.doctor),
            joinedload(MedicalStudy.technician)
        ).filter(MedicalStudy.id == study_id).first()
        
        if not study:
            return None
        
        # Debug: verificar datos antes de convertir a DTO
        print(f"=== GET BY ID DEBUG ===")
        print(f"Study ID: {study.id}")
        print(f"Access Code: {study.access_code}")
        print(f"Creation Date: {study.created_at}")
        print(f"Creation Date Type: {type(study.created_at)}")
        print(f"Patient: {study.patient.name if study.patient else 'None'}")
        print(f"Patient Email: {study.patient.email if study.patient else 'None'}")
        print(f"Doctor: {study.doctor.name if study.doctor else 'None'}")
        print(f"Doctor Email: {study.doctor.email if study.doctor else 'None'}")
        print(f"Technician: {study.technician.name if study.technician else 'None'}")
        print(f"======================")
        
        try:
            dto = MedicalStudyResponseDTO.model_validate(study)
            print(f"DTO Creation Date: {dto.creation_date}")
            print(f"DTO Patient Email: {dto.patient.email if dto.patient else 'None'}")
            return dto
        except Exception as e:
            print(f"Error validating study {study.id}: {e}")
            raise e
    
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
    
    def get_all_studies(self, db: Session) -> List[MedicalStudyResponseDTO]:
        """
        Obtiene todos los estudios médicos y los convierte a DTO.
        """
        studies = self.__medical_study_repo.get_all(db)
        
        # Convertir cada objeto MedicalStudy a MedicalStudyResponseDTO
        return [
            MedicalStudyResponseDTO.model_validate(study) 
            for study in studies
        ]

    def delete_study(self, db: Session, study_id: UUID):
        """
        Verifica que un estudio exista y luego lo elimina.
        """
        # Reutilizamos el método get_study para manejar el caso de que no exista (error 404)
        study_to_delete = self.get_by_id(db, study_id=study_id)
        
        # Si existe, llama al repositorio para eliminarlo
        return self.__medical_study_repo.delete(db, id=study_to_delete.id)

    def update(self, db: Session, *, study_id: UUID, study_update: MedicalStudyUpdateDTO):
        """
        Actualiza un estudio médico de forma parcial (PATCH).
        """
        # 1. Obtener el objeto de BD directamente usando get_by_id
        db_study = self.__medical_study_repo.get_by_id(db, id=study_id)  # ← CAMBIO: usar get_by_id
        if not db_study:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medical study with ID {study_id} not found."
            )
        
        # 2. Convertir el DTO a diccionario
        update_data = study_update.model_dump(exclude_unset=True)

        # 3. Validaciones de negocio (si necesitas)
        if "doctor_id" in update_data:
            new_doctor_id = update_data["doctor_id"]
            doctor = self.__user_repo.get(db, id=new_doctor_id)
            if not doctor or "DOCTOR" not in [role.name for role in doctor.roles]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid new Doctor ID: {new_doctor_id}")
        
        # 4. Actualizar y devolver como DTO
        updated_study = self.__medical_study_repo.update(db, db_obj=db_study, obj_in=update_data)
        return MedicalStudyResponseDTO.model_validate(updated_study)