package com.VikingLabs.MielIA.Config;

import io.swagger.v3.oas.models.ExternalDocumentation;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;

@Configuration
public class SwaggerConfig {

    @Value("${application.address}")
    private String serverAddress;

    @Value("${application.port}")
    private String serverPort;

    @Value("${server.servlet.context-path:/}")
    private String contextPath;

    @Bean
    public OpenAPI customOpenAPI() {
        String serverUrl = String.format("http://%s:%s%s",
                serverAddress,
                serverPort,
                contextPath.equals("/") ? "" : contextPath);

        String description = """
            # MielIA - Sistema de Apoyo al Diagnóstico del Síndrome de Guillain-Barré
            
            ## 📌 Descripción General
            API REST para análisis de datos clínicos y apoyo al diagnóstico del Síndrome de Guillain-Barré (SGB).
            
            ## 🔓 Estado Actual
            - **Sin autenticación**: Todos los endpoints son públicos (etapa de desarrollo).
            - **Integración con modelos de ML**: Procesa síntomas y resultados de pruebas.
            
            ## 📊 Flujo de Trabajo
            1. Registro de pacientes → 2. Carga de datos → 3. Obtención de resultados
            """;

        return new OpenAPI()
                .servers(Arrays.asList(
                        new Server()
                                .url(serverUrl)
                                .description("Servidor principal")
                ))
                .info(new Info()
                        .title("MielIA API")
                        .description(description)
                        .version("1.0")
                        .contact(new Contact()
                                .name("Equipo MielIA")
                                .email("mirazopablo@gmail.com")
                                .url("https://miel-ia.org"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")))
                .externalDocs(new ExternalDocumentation()
                        .description("Documentación Técnica")
                        .url("https://docs.miel-ia.org"));
    }
    @PostConstruct
    public void printOpenApiUrls() {
        String baseUrl = String.format("http://%s:%s%s",
                serverAddress,
                serverPort,
                contextPath.equals("/") ? "" : contextPath);

        System.out.println("\n========= OpenAPI URLs =========");
        System.out.println("Swagger UI: " + baseUrl + "/swagger-ui.html");
        System.out.println("API Docs: " + baseUrl + "/v3/api-docs");
        System.out.println("================================\n");
    }
}