# Ticket de Turno

Sistema de agendamiento de citas escolares para el sector educativo del estado de Coahuila.

## 1. Descripción
Aplicación Desktop (MVC) para gestionar solicitudes de trámites escolares. Los padres registran datos de sus hijos para generar un comprobante (Ticket), y los administradores gestionan y resuelven las solicitudes.

## 2. Arquitectura
La aplicación sigue un estricto patrón **MVC (Model-View-Controller)** en capas:
- **Models**: Contiene las entidades y la lógica de negocio básica (ej. cálculo de nombre completo).
- **Views**: Interfaces gráficas creadas en PyQt6. Libres de lógica o acceso a base de datos.
- **Controllers**: Coordinadores que reciben señales de las vistas, hablan con los `Repositories` y usan el `EventBus` para notificar del nuevo estado.
- **Repositories**: Capa de abstracción sobre la BD SQLite.

## 3. Patrones de Diseño
### Repository Pattern
Separa el SQL de los controladores mediante una interfazCRUD abstracta.
```python
class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self): pass
```

### Observer Pattern (EventBus)
Desacopla componentes enviando eventos. Por ejemplo, al cambiar un estatus, el Dashboard re-dibuja el KPI:
```python
EventBus().publish(AppEvent.ESTATUS_CAMBIADO, ...)
```

## 4. Instalación y Ejecución
1. Verifica Python 3.11+: `python --version`
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # En windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar app:
   ```bash
   python main.py
   ```

## 5. Capturas de pantalla
*(Incluir imágenes del registro, panel admin y dashboard aquí)*

## 6. Modelo de Datos
*(Incluir er_diagram.png aquí)*

## 7. Diagrama de Clases
*(Incluir classes_TicketDeTurno.png aquí)*

## 8. Decisiones Técnicas
- **SQLite**: No requiere instalación de servidor, ideal para una aplicación de escritorio distribuible.
- **PyQt6**: Binding oficial y moderno para UI nativa de Qt. Soporta estilos CSS completos.
- **Patrones aplicados**: Maximizan la escalabilidad y limpieza (SOLID).

## 9. Credenciales de Demo
- **Usuario:** admin
- **Clave:** Admin123!

## 10. Autores
- David Eduardo Lara Flores
- Miguel Arrollo Lopez
