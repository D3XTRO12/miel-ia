package com.VikingLabs.MielIA.DTOs;

import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.*;
import lombok.Data;

import java.util.UUID;

@Data
@Tag(name="DTO", description = "Data Transfer Objects")
@Schema(name = "MedicalStudyDTO", description = "DTO para creación y visualización de estudios médicos")
public class MedicalStudyDTO {

    @Schema(description = "ID del paciente", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotNull(message = "El ID del paciente es obligatorio")
    private UUID patientId;

    @Schema(description = "ID del médico", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotNull(message = "El ID del médico es obligatorio")
    private UUID doctorId;

    @Schema(description = "ID del técnico (opcional)")
    private UUID technicianId;

    @Schema(description = "Código de acceso de 4 caracteres", requiredMode = Schema.RequiredMode.REQUIRED)
    @Size(min = 4, max = 4, message = "El código debe tener exactamente 4 caracteres")
    private String accessCode;

    @Schema(description = "Datos clínicos en formato JSON", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "Los datos clínicos son obligatorios")
    private String clinicalData;
}