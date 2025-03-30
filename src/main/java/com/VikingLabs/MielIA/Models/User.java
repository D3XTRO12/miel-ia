package com.VikingLabs.MielIA.Models;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Tag(name="Models")
@Schema(
        description = "Entidad que representa un usuario en el sistema",
        name = "User"  // Nombre claro para Swagger UI
)
@Entity
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "users")
public class User {

    @Schema(
            description = "Identificador único del usuario",
            example = "123e4567-e89b-12d3-a456-426614174000",
            requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Schema(
            description = "Nombre del usuario",
            example = "Juan",
            maxLength = 50,
            requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Column(name = "name", nullable = false, length = 50)
    private String name;

    @Schema(
            description = "Apellido del usuario",
            example = "Perez",
            maxLength = 50,
            requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;

    @Schema(
            description = "DNI del usuario",
            example = "12345678",
            minLength = 8,
            maxLength = 15,
            requiredMode = Schema.RequiredMode.REQUIRED
    )
    @Column(name = "dni", nullable = false, length = 15)
    private String dni;

    @Schema(
            description = "Correo electrónico del usuario",
            example = "someone@example.com",
            format = "email",
            maxLength = 100
    )
    @Column(name = "email", length = 100)
    private String email;

    @Schema(
            description = "Contraseña del usuario (encriptada)",
            example = "$2a$10$N9qo8uLOickgx2ZMRZoMy...",
            requiredMode = Schema.RequiredMode.REQUIRED,
            accessMode = Schema.AccessMode.READ_ONLY  // No debería mostrarse en responses
    )
    @Column(name = "password", nullable = false)
    private String password;

    @Schema(
            description = "Roles asignados al usuario",
            implementation = UserRole.class
    )
    @JsonManagedReference
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<UserRole> userRoles = new HashSet<>();
}