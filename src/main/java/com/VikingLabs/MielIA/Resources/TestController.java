package com.VikingLabs.MielIA.Resources;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "Test")
@RequestMapping("/api/test")
public class TestController {

    @Operation(summary = "Endpoint de prueba")
    @GetMapping
    public String test() {
        return "Swagger funciona!";
    }
}