-- Catálogo de municipios de Coahuila
CREATE TABLE IF NOT EXISTS municipios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    activo      INTEGER DEFAULT 1
);

-- Catálogo de niveles educativos
CREATE TABLE IF NOT EXISTS niveles_educativos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    activo      INTEGER DEFAULT 1
);

-- Catálogo de asuntos/trámites
CREATE TABLE IF NOT EXISTS asuntos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL UNIQUE,
    activo      INTEGER DEFAULT 1
);

-- Usuarios administradores
CREATE TABLE IF NOT EXISTS usuarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    activo          INTEGER DEFAULT 1,
    creado_en       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal: Alumnos (PK = CURP)
CREATE TABLE IF NOT EXISTS alumnos (
    curp            TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    paterno         TEXT NOT NULL,
    materno         TEXT NOT NULL,
    nivel_id        INTEGER NOT NULL,
    municipio_id    INTEGER NOT NULL,
    FOREIGN KEY (nivel_id)     REFERENCES niveles_educativos(id),
    FOREIGN KEY (municipio_id) REFERENCES municipios(id)
);

-- Tabla de solicitudes/tickets
CREATE TABLE IF NOT EXISTS solicitudes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_turno        INTEGER NOT NULL,
    curp_alumno         TEXT NOT NULL,
    quien_tramita       TEXT NOT NULL,
    telefono_principal  TEXT NOT NULL,
    telefono_secundario TEXT,
    correo              TEXT NOT NULL,
    asunto_id           INTEGER NOT NULL,
    municipio_id        INTEGER NOT NULL,
    estatus             TEXT NOT NULL DEFAULT 'Pendiente' CHECK(estatus IN ('Pendiente','Resuelto')),
    observaciones       TEXT,
    creado_en           DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curp_alumno)  REFERENCES alumnos(curp),
    FOREIGN KEY (asunto_id)    REFERENCES asuntos(id),
    FOREIGN KEY (municipio_id) REFERENCES municipios(id)
);

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_solicitudes_curp       ON solicitudes(curp_alumno);
CREATE INDEX IF NOT EXISTS idx_solicitudes_municipio  ON solicitudes(municipio_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_estatus    ON solicitudes(estatus);
CREATE UNIQUE INDEX IF NOT EXISTS idx_turno_municipio ON solicitudes(numero_turno, municipio_id);

-- Trigger: actualizar timestamp en UPDATE
CREATE TRIGGER IF NOT EXISTS trg_solicitud_update
AFTER UPDATE ON solicitudes
BEGIN
    UPDATE solicitudes SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Datos semilla

INSERT OR IGNORE INTO municipios (nombre) VALUES 
('Abasolo'), ('Acuña'), ('Allende'), ('Arteaga'), ('Candela'),
('Castaños'), ('Cuatro Cienégas'), ('Escobedo'), ('Francisco I. Madero'), ('Frontera'),
('General Cepeda'), ('Guerrero'), ('Hidalgo'), ('Jiménez'), ('Juárez'),
('Lamadrid'), ('Matamoros'), ('Monclova'), ('Morelos'), ('Múzquiz'),
('Nadadores'), ('Nava'), ('Ocampo'), ('Parras'), ('Piedras Negras'),
('Progreso'), ('Ramos Arizpe'), ('Sabinas'), ('Sacramento'), ('Saltillo'),
('San Buenaventura'), ('San Juan de Sabinas'), ('San Pedro'), ('Sierra Mojada'), ('Torreón'),
('Viesca'), ('Villa Unión'), ('Zaragoza');

INSERT OR IGNORE INTO niveles_educativos (nombre) VALUES 
('Preescolar'), ('Primaria'), ('Secundaria'), ('Preparatoria/Bachillerato'), ('Universidad');

INSERT OR IGNORE INTO asuntos (descripcion) VALUES 
('Inscripción'), ('Reinscripción'), ('Beca'), ('Traslado'), ('Calificaciones'), ('Certificado'), ('Otro');

-- Contraseña hasheada (Admin123!) usando bcrypt (pre-generado)
INSERT OR IGNORE INTO usuarios (username, password_hash, nombre_completo) VALUES 
('admin', '$2b$12$rJXAOYbEZD.LbJE5atdMFuL4P0OwQjP6SVDlsw5dvbYk1VuQvWYH.', 'Administrador del Sistema');

-- Tabla de Bitácora de Auditoría para registrar acciones críticas del sistema
CREATE TABLE IF NOT EXISTS bitacora (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario     TEXT NOT NULL,
    accion      TEXT NOT NULL,
    detalle     TEXT NOT NULL,
    creado_en   DATETIME DEFAULT CURRENT_TIMESTAMP
);

