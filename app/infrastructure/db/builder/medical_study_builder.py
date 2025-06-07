from ..dataclass.medical_study import MedicalStudy

class MedicalStudyBuilder:
    def __init__(self, access_code, clinical_data, ml_results, status, doctor_id, patient_id, technician_id, csv_file_id):
        self.medical_study = MedicalStudy()
        self.medical_study.access_code = access_code
        self.medical_study.clinical_data = clinical_data
        self.medical_study.ml_results = ml_results
        self.medical_study.status = status
        self.medical_study.doctor_id = doctor_id
        self.medical_study.patient_id = patient_id
        self.medical_study.technician_id = technician_id
        self.medical_study.csv_file_id = csv_file_id

    def build(self):
        return self.medical_study
