package com.VikingLabs.MielIA.Models;

import com.fasterxml.jackson.annotation.JsonBackReference;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Schema(description = "Entidad que relaciona los usuarios con su rol")
@Entity
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user_roles")
public class UserRole {

    @Schema(description = "Identificador único de la relación entre usuario y rol", example = "123e4567-e89b-12d3-a456-426614174000")
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private String id;

    @Schema(description = "ID del Usuario al que se le asigna el rol")
    @ManyToOne
    @JsonBackReference // Indica que esta es la parte "no propietaria" de la relación
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Schema(description = "ID del Rol que se le asigna al usuario")
    @ManyToOne
    @JsonBackReference // Indica que esta es la parte "no propietaria" de la relación
    @JoinColumn(name = "role_id", nullable = false)
    private Role role;

    
}
