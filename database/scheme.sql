DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE rol (
  id SERIAL PRIMARY KEY,
  tipo TEXT NOT NULL
);

CREATE TABLE usuario (
  correo VARCHAR(255) NOT NULL PRIMARY KEY CHECK (correo LIKE '%@_%.%'),
  contrasena TEXT NOT NULL CHECK (contrasena ~ '^(?=.*[A-Z])(?=.*\d).{6,8}$'),
  rol_id INTEGER NOT NULL REFERENCES rol(id)
);

CREATE TABLE administrador (
  correo_administrador TEXT NOT NULL PRIMARY KEY REFERENCES usuario(correo)
);

CREATE TABLE miembro (
  correo_miembro TEXT NOT NULL PRIMARY KEY REFERENCES usuario(correo),
  nombre TEXT NOT NULL,
  edad INTEGER NOT NULL,
  direccion TEXT NOT NULL,
  telefono TEXT NOT NULL,
  fecha_vencimiento DATE NOT NULL,
  tipo_membresia TEXT NOT NULL
);

CREATE TABLE instructor (
  nombre TEXT PRIMARY KEY
);

CREATE TABLE clase (
  id TEXT PRIMARY KEY,
  nombre_instructor TEXT NOT NULL REFERENCES instructor(nombre),
  horario TIME NOT NULL
);

CREATE TABLE asiste (
  correo_miembro TEXT NOT NULL REFERENCES miembro(correo_miembro),
  id_clase TEXT NOT NULL REFERENCES clase(id),
  fecha_asistencia DATE NOT NULL
);

INSERT INTO rol (tipo)
VALUES 
('Administrador'),
('Miembro');

INSERT INTO usuario (correo, contrasena, rol_id)
VALUES
('gimnasiocarlos@gmail.com', 'CNaRa11Z', 1),
('usuario1@example.com', 'Pass123', 2),
('usuario2@example.com', 'P4ss789', 2),
('usuario3@example.com', 'Secu01', 2),
('usuario4@example.com', 'MyP@02', 2),
('usuario5@example.com', 'Stro0rd', 2);

INSERT INTO administrador (correo_administrador)
VALUES ('gimnasiocarlos@gmail.com');

INSERT INTO miembro (correo_miembro, nombre, edad, direccion, telefono, fecha_vencimiento, tipo_membresia) 
VALUES
('usuario1@example.com', 'Juan Pérez', 25, 'Calle 123, Ciudad', '555-1234', '2024-05-31', 'Premium'),
('usuario2@example.com', 'María Gómez', 30, 'Av. Principal, Pueblo', '555-5678', '2023-07-15', 'Básica'),
('usuario3@example.com', 'Pedro Jiménez', 40, 'C/ Mayor, Villa', '555-9012', '2023-12-31', 'Premium'),
('usuario4@example.com', 'Ana Torres', 35, 'Plaza Central, Ciudad', '555-3456', '2022-11-30', 'Básica'),
('usuario5@example.com', 'Luisa Fernández', 28, 'C/ Secundaria, Pueblo', '555-7890', '2024-08-18', 'Premium');

INSERT INTO instructor (nombre) 
VALUES
('Instructor A'),
('Instructor B'),
('Instructor C'),
('Instructor D'),
('Instructor E');

INSERT INTO clase (id, nombre_instructor, horario) 
VALUES
('Clase1', 'Instructor A', '14:00:00'),
('Clase2', 'Instructor B', '18:30:00'),
('Clase3', 'Instructor C', '10:00:00'),
('Clase4', 'Instructor D', '17:00:00'),
('Clase5', 'Instructor E', '15:30:00');

INSERT INTO asiste (correo_miembro, id_clase, fecha_asistencia) 
VALUES
('usuario1@example.com', 'Clase1', '2023-05-31'),
('usuario2@example.com', 'Clase2', '2023-05-31');