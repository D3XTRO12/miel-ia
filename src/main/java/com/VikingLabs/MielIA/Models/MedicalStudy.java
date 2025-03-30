package com.VikingLabs.MielIA.Models;

import com.fasterxml.jackson.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "medical_studies")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Entidad que representa un estudio médico del Síndrome de Guillain-Barré")
public class MedicalStudy {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(columnDefinition = "BINARY(16)")
    @Schema(description = "ID único del estudio", example = "123e4567-e89b-12d3-a456-426614174000")
    private UUID id;

    // Patient relationship
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "patient_id", nullable = false)
    @JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
    @JsonIdentityReference(alwaysAsId = true)
    @JsonProperty("patientId")
    @Schema(description = "ID del paciente asociado", example = "550e8400-e29b-41d4-a716-446655440000")
    private User patient;

    // Doctor relationship
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "doctor_id", nullable = false)
    @JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
    @JsonIdentityReference(alwaysAsId = true)
    @JsonProperty("doctorId")
    @Schema(description = "ID del médico responsable", example = "6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    private User doctor;

    // Technician relationship (optional)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "technician_id")
    @JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
    @JsonIdentityReference(alwaysAsId = true)
    @JsonProperty("technicianId")
    @Schema(description = "ID del técnico que realizó el estudio", example = "6ba7b811-9dad-11d1-80b4-00c04fd430c9")
    private User technician;

    @Column(nullable = false, unique = true, length = 4)
    @Schema(description = "Código alfanumérico de 4 dígitos para acceso seguro",
            example = "A1B2", minLength = 4, maxLength = 4)
    private String accessCode;

    @Column(nullable = false)
    @Schema(description = "Fecha y hora de creación del estudio", example = "2025-03-21T10:30:00")
    private LocalDateTime creationDate = LocalDateTime.now();

    @Column(nullable = false)
    @Schema(description = "Estado del estudio", example = "EN_PROCESO")
    private String status = "IN_PROGRESS";

    @Lob
    @Schema(description = "Datos clínicos del estudio en formato JSON")
    private String clinicalData;

    @Lob
    @Schema(description = "Resultados del modelo de ML en formato JSON")
    private String mlResults;

    // Helper methods to prevent recursion
    @JsonGetter("patientId")
    public UUID getPatientId() {
        return patient != null ? patient.getId() : null;
    }

    @JsonGetter("doctorId")
    public UUID getDoctorId() {
        return doctor != null ? doctor.getId() : null;
    }

    @JsonGetter("technicianId")
    public UUID getTechnicianId() {
        return technician != null ? technician.getId() : null;
    }
}