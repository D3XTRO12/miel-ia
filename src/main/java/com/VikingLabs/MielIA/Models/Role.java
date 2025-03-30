package com.VikingLabs.MielIA.Models;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Schema(description = "Entidad que representa un rol en el sistema")
@Entity
@Setter
@Getter
@Table(name = "roles")
@NoArgsConstructor
@AllArgsConstructor
public class Role {

    @Schema(description = "Identificador único del rol con formato UUID", example = "123e4567-e89b-12d3-a456-426614174000")
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", updatable = false, nullable = false)
    private String id;

    @Schema(description = "Nombre del rol", example = "ADMIN")
    @Column(name = "name", nullable = false)
    private String name;

    @JsonManagedReference
    @OneToMany(mappedBy = "role", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<UserRole> userRoles = new HashSet<>();

}

