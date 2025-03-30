package com.VikingLabs.MielIA.DTOs;

import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;
import java.util.UUID;

@Data
@Tag(name="DTO", description = "Data Transfer Objects")
@NoArgsConstructor
@AllArgsConstructor
@Schema(
        name = "UserDTO",
        description = "Objeto de Transferencia de Datos para operaciones con Usuarios"
)
public class UserDTO {

    @Schema(
            description = "ID único del usuario (solo para respuestas)",
            example = "123e4567-e89b-12d3-a456-426614174000",
            accessMode = Schema.AccessMode.READ_ONLY
    )
    private UUID id;

    @Schema(
            description = "Nombre del usuario",
            example = "Juan",
            requiredMode = Schema.RequiredMode.REQUIRED,
            maxLength = 50
    )
    @NotBlank(message = "El nombre es obligatorio")
    @Size(max = 50, message = "El nombre no puede exceder los 50 caracteres")
    private String name;

    @Schema(
            description = "Apellido del usuario",
            example = "Perez",
            requiredMode = Schema.RequiredMode.REQUIRED,
            maxLength = 50
    )
    @NotBlank(message = "El apellido es obligatorio")
    @Size(max = 50, message = "El apellido no puede exceder los 50 caracteres")
    private String lastName;

    @Schema(
            description = "DNI del usuario (solo números)",
            example = "12345678",
            requiredMode = Schema.RequiredMode.REQUIRED,
            minLength = 8,
            maxLength = 15
    )
    @NotBlank(message = "El DNI es obligatorio")
    @Size(min = 8, max = 15, message = "El DNI debe tener entre 8 y 15 caracteres")
    @Pattern(regexp = "^[0-9]+$", message = "El DNI solo debe contener números")
    private String dni;

    @Schema(
            description = "Correo electrónico válido",
            example = "usuario@example.com",
            requiredMode = Schema.RequiredMode.REQUIRED,
            format = "email"
    )
    @NotBlank(message = "El email es obligatorio")
    @Email(message = "Debe ser un email válido")
    @Size(max = 100, message = "El email no puede exceder los 100 caracteres")
    private String email;

    @Schema(
            description = "Contraseña (solo para creación/actualización)",
            example = "MiContraseñaSegura123!",
            requiredMode = Schema.RequiredMode.REQUIRED,
            minLength = 8,
            maxLength = 30,
            accessMode = Schema.AccessMode.WRITE_ONLY
    )
    @NotBlank(message = "La contraseña es obligatoria")
    @Size(min = 8, max = 30, message = "La contraseña debe tener entre 8 y 30 caracteres")
    private String password;

    @Schema(
            description = "Roles del usuario (IDs de roles)",
            example = "[1, 2]",
            requiredMode = Schema.RequiredMode.NOT_REQUIRED
    )
    private Set<Long> roleIds;
}