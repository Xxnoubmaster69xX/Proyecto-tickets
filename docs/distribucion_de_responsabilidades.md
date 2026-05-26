# 📋 Distribución de Responsabilidades y Tareas — Ticket de Turno

**Materia:** Diseño y Arquitectura de Software  
**Proyecto:** Aplicación Desktop "Ticket de Turno"  
**Equipo:** 2 Integrantes  
**Fecha de Entrega:** 2026-05-26  

---

## 👥 Integrantes del Equipo

1. **David Eduardo Lara Flores** (GitHub: `Xxnoubmaster69xX`)
2. **Miguel Arrollo Lopez** (GitHub: `Mike-5050` / `DAvoid`)

---

## 📊 Asignación de Puntos Operacionales y Técnicos

A continuación se detalla la asignación de responsabilidades de desarrollo y documentación para cada integrante del equipo, cubriendo los puntos de evaluación del parcial.

### 👤 David Eduardo Lara Flores (`Xxnoubmaster69xX`)

| Punto Evaluado | Tarea / Componente Desarrollado | Descripción Técnica |
| :--- | :--- | :--- |
| **Requisito Técnico 1, 2, 3** | Arquitectura MVC, Base de Datos y OOP | Implementación de las clases base, entidades del modelo (`Alumno`, `Solicitud`, `Usuario`), y configuración de la persistencia relacional con SQLite (`DatabaseConnection` en Singleton y `schema.sql`). |
| **Requisito Técnico 4, 5** | Patrón Repository | Creación de la capa de acceso a datos (`BaseRepository`, `AlumnoRepository`, `SolicitudRepository`, `CatalogoRepository`) abstrayendo completamente las consultas SQL de los controladores. |
| **Requisito Operacional 6** | Formulario Público de Registro y Modificación | Diseño y lógica de la vista `SolicitudPublicaView`, permitiendo a los usuarios registrar solicitudes y modificarlas utilizando únicamente su CURP y el Número de Turno asignado. |
| **Requisito Operacional 9** | Generación de Turno Secuencial por Municipio | Implementación de la lógica en base de datos (`get_next_turno_for_municipio`) para asignar turnos independientes de $1$ a $n$ por cada municipio de Coahuila. |
| **Requisito Operacional 11** | Validación de CURP Oficial | Creación de la lógica de validación mediante expresiones regulares en `curp_validator.py`, garantizando la correcta composición técnica y el cumplimiento de las restricciones oficiales (incluyendo dígitos alfanuméricos verificadores). |
| **Requisito Operacional 2 y 8** | CRUD Completo de Catálogos | Vista y lógica para la administración y edición directa de catálogos (`catalogos_view.py`) para los municipios, asuntos y niveles educativos. |

---

### 👤 Miguel Arrollo Lopez (`Mike-5050` / `DAvoid`)

| Punto Evaluado | Tarea / Componente Desarrollado | Descripción Técnica |
| :--- | :--- | :--- |
| **Requisito Operacional 10** | Tablero de Control (Dashboard) | Implementación de la vista `dashboard_view.py` y `dashboard_controller.py`, integrando gráficos estadísticos mediante `matplotlib` (gráfico de pastel de estatus y barra horizontal de asuntos/municipios) y filtros dinámicos. |
| **Requisito Operacional 1** | Login de Seguridad para Admin | Implementación de la autenticación de usuarios administradores (`login_view.py`), incluyendo el hash de contraseñas de manera segura a través de la librería `bcrypt` en la base de datos. |
| **Requisito Operacional 3** | Menú, Navegación y Seguridad | Estructura de la ventana principal (`main_window.py`) con barra de menú dinámica, manejo del estado de sesión global (`SessionManager` en Singleton), control de logout y cierre seguro de la conexión SQLite. |
| **Requisito Operacional 5** | Patrón Observer (EventBus) | Creación e integración del bus de eventos desacoplado (`patterns/event_bus.py`) para notificar cambios de estado en tiempo real (por ejemplo, actualizar el dashboard automáticamente tras resolver un ticket). |
| **Documentación** | Modelado de Software y Presentación de Patrones | Diseño y renderizado de los diagramas UML oficiales (`diagrama_clases.puml`, `database_er_diagram.puml` y `diagrama_arquitectura.puml`) y desarrollo de la presentación interactiva de patrones de diseño (`patrones_de_diseno.html`). |
| **Pruebas y QA** | Automatización de Datos de Demo | Creación del script `populate_data.sql` con más de 360 registros simulados en la base de datos para realizar pruebas de estrés de los algoritmos y demostrar el dashboard en la exposición. |

---

## 🛠️ Firmas de Conformidad

Este documento certifica el reparto equitativo del trabajo técnico del proyecto y es entregado en tiempo y forma para derecho a evaluación parcial.

```
__________________________________
David Eduardo Lara Flores
Desarrollador Core / Base de Datos
```

```
__________________________________
Miguel Arrollo Lopez
Desarrollador UI / Documentación y UML
```
