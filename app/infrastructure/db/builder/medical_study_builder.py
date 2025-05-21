from ..dataclass.medical_study import MedicalStudy

class MedicalStudieBuilder:
    def __init__(self, access_code, clinical_data, ml_results, status, doctor_id, patient_id, technician_id):
        self.medical_studie = MedicalStudy()
        self.medical_studie.access_code = access_code
        self.medical_studie.clinical_data = clinical_data
        self.medical_studie.ml_results = ml_results
        self.medical_studie.status = status
        self.medical_studie.doctor_id = doctor_id
        self.medical_studie.patient_id = patient_id
        self.medical_studie.technician_id = technician_id

    def build(self):
        return self.medical_studie
