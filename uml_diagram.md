# Arquitectura y Estructura del Sistema (Ticket de Turno)

A continuación te presento los diagramas solicitados generados a **nivel senior** mostrando los patrones de diseño (Repository, REST API, Client-Server MVC) y las interacciones de base de datos.

## 1. Arquitectura del Sistema (Despliegue General)

```mermaid
graph TD
    subgraph Frontend ["Frontend (SPA React + Vite)"]
        UI[UI Components]
        Pages[Views: Login, Dashboard, Public...]
        Router[React Router]
        Pages --> UI
        Router --> Pages
    end

    subgraph API ["Backend REST API (FastAPI)"]
        Controllers[API Routers / Endpoints]
        Schemas[Pydantic Validation Schemas]
        Services[Business Logic & Ticket Gen]
        Repos[Repositories Pattern]
        
        Controllers --> Schemas
        Controllers --> Services
        Services --> Repos
    end

    subgraph Database ["SQLite Database"]
        DB[(ticket_turno.db)]
    end

    %% Conexiones
    Pages -- "HTTP/JSON" --> Controllers
    Repos -- "SQL Queries" --> DB
```

> [!NOTE]
> Se utiliza el **Patrón Cliente-Servidor**. Toda la responsabilidad de renderizado (MVC) recae en el Frontend React, mientras que el Backend Python se reduce exclusivamente a una API REST transaccional que emite JSON. 

---

## 2. Diagrama de Clases UML (Dominio Backend)

Este diagrama modela la lógica de las entidades de negocio y la separación de responsabilidades usando el **Patrón Repositorio**.

```mermaid
classDiagram
    %% Entidades
    class BaseModel {
        <<abstract>>
        +int id
    }
    
    class Alumno {
        +String curp
        +String nombre
        +String paterno
        +String materno
        +int nivel_id
        +int municipio_id
    }
    
    class Solicitud {
        +String curp_alumno
        +int numero_turno
        +int asunto_id
        +String quien_tramita
        +String telefono_principal
        +String correo
        +String estatus
        +DateTime fecha_registro
    }

    class Municipio {
        +String nombre
    }
    
    class NivelEducativo {
        +String nombre
    }

    class Asunto {
        +String descripcion
    }

    %% Relaciones
    BaseModel <|-- Alumno
    BaseModel <|-- Municipio
    BaseModel <|-- NivelEducativo
    BaseModel <|-- Asunto
    
    Alumno "1" --> "1" Municipio : Pertenece
    Alumno "1" --> "1" NivelEducativo : Cursa
    Solicitud "*" --> "1" Alumno : Registra
    Solicitud "*" --> "1" Asunto : Trata sobre

    %% Repositorios (Patrón de acceso a datos)
    class BaseRepository {
        <<interface>>
        +get_all()
        +get_by_id(id)
        +insert(model)
        +update(model)
        +delete(id)
    }

    class SolicitudRepository {
        +get_pendientes()
        +get_stats_dashboard()
        +generate_ticket_number(municipio_id)
        +buscar_por_curp(curp)
    }

    class CatalogoRepository {
        +get_municipios()
        +get_niveles()
        +get_asuntos()
    }

    BaseRepository <|-- SolicitudRepository
    BaseRepository <|-- CatalogoRepository

    %% Dependencias
    SolicitudRepository ..> Solicitud : manipula
    CatalogoRepository ..> Municipio : manipula
```

> [!TIP]
> **Desacoplamiento Senior:** Al tener una capa `BaseRepository`, si mañana cambias `SQLite` por `PostgreSQL` o `MySQL`, tu capa de controladores (API) no sufriría ninguna modificación, protegiendo así la escalabilidad de tu app.
