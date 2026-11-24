--Base de datos para el proyecto
--IT

Create database GestionIT
use GestionIT

go

Create table cliente(
DUIcl int not null primary key,
Nombre varchar(25) not null,
Apellido varchar(25) not null,
telefono varchar(9) not null,
direccion varchar(60) not null,
correo varchar(50) not null,
)

CREATE TABLE sucursal (
    idSucursal INT NOT NULL PRIMARY KEY,
    Sucursal VARCHAR(80) NOT NULL,
    numerotelefono VARCHAR(8) NOT NULL
)

CREATE TABLE roles (
    IDRol INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    NombreRol VARCHAR(25) NOT NULL UNIQUE
)

CREATE TABLE categorias (
    IDCategoria INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    NombreCategoria VARCHAR(50) NOT NULL
)

CREATE TABLE marcas (
    IDMarca INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    NombreMarca VARCHAR(50) NOT NULL
)

CREATE TABLE servicios (
    IDServicio INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    NombreServicio VARCHAR(50) NOT NULL,
    CostoServicio DECIMAL(10,2) NOT NULL CHECK (CostoServicio >= 0),
    Descripcion VARCHAR(100) NULL
)

CREATE TABLE Empleado(
    IDemp int not null primary key,
    nombreEMP varchar(30) not null,
    apellido varchar(20) not null,
    Rol varchar(20) not null,
    IDRol INT NULL,
    idSucursal INT NULL,
    CONSTRAINT FK_Empleado_rol FOREIGN KEY (IDRol) REFERENCES roles(IDRol),
    CONSTRAINT FK_Empleado_sucursal FOREIGN KEY (idSucursal) REFERENCES sucursal(idSucursal)
)

CREATE TABLE usuarios_empleado (
    IDUsuario INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    IDemp INT NOT NULL UNIQUE,
    Usuario VARCHAR(30) NOT NULL UNIQUE,
    Clave VARCHAR(100) NOT NULL,
    Activo BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_usuarios_empleado FOREIGN KEY (IDemp) REFERENCES Empleado(IDemp)
)
CREATE TABLE productos (
    IDprod INT NOT NULL PRIMARY KEY,
    nombreProd VARCHAR(30) NOT NULL,
    costoprod DECIMAL(10,2) NOT NULL CHECK (costoprod >= 0),
    existencias INT NOT NULL CHECK (existencias >= 0),
    descripcion VARCHAR(50) NULL,
    IDCategoria INT NULL,
    IDMarca INT NULL,
    SKU VARCHAR(30) NULL,
    ImagenURL VARCHAR(255) NULL,
    CONSTRAINT FK_productos_categoria FOREIGN KEY (IDCategoria) REFERENCES categorias(IDCategoria),
    CONSTRAINT FK_productos_marca FOREIGN KEY (IDMarca) REFERENCES marcas(IDMarca)
)

--Alguien puede hacer las foreign key para referenciar los clientes, sucursal,empleado, producto
--Si hay mas ideas podemos agregar otra tabla para agregar mas servicios
--Como mantenimiento, reparacion etc etc.
Create table factura(
    IDfact INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    empleFACT INT NOT NULL,
    sucurFACT INT NOT NULL,
    prodFACT INT NULL,
    ClienFACT INT NOT NULL,
    IDServicio INT NULL,
    FechaFactura DATETIME NOT NULL DEFAULT GETDATE(),
    Total DECIMAL(10,2) NULL CHECK (Total >= 0),
    EstadoPedido VARCHAR(25) NOT NULL DEFAULT 'Completada',
    ModalidadEntrega VARCHAR(25) NOT NULL DEFAULT 'Sucursal',
    CONSTRAINT FK_factura_cliente FOREIGN KEY (ClienFACT) REFERENCES cliente(DUIcl),
    CONSTRAINT FK_factura_sucursal FOREIGN KEY (sucurFACT) REFERENCES sucursal(idSucursal),
    CONSTRAINT FK_factura_empleado FOREIGN KEY (empleFACT) REFERENCES Empleado(IDemp),
    CONSTRAINT FK_factura_producto FOREIGN KEY (prodFACT) REFERENCES productos(IDprod),
    CONSTRAINT FK_factura_servicio FOREIGN KEY (IDServicio) REFERENCES servicios(IDServicio)
)

CREATE TABLE detalle_factura (
    IDDetalle INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    IDfact INT NOT NULL,
    IDprod INT NULL,
    IDServicio INT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    PrecioUnitario DECIMAL(10,2) NOT NULL CHECK (PrecioUnitario >= 0),
    Subtotal AS (Cantidad * PrecioUnitario) PERSISTED,
    CONSTRAINT FK_detalle_factura FOREIGN KEY (IDfact) REFERENCES factura(IDfact),
    CONSTRAINT FK_detalle_producto FOREIGN KEY (IDprod) REFERENCES productos(IDprod),
    CONSTRAINT FK_detalle_servicio FOREIGN KEY (IDServicio) REFERENCES servicios(IDServicio)
)

CREATE VIEW vw_LoginEmpleados AS
SELECT
    u.IDUsuario,
    u.Usuario,
    u.Clave,
    u.Activo,
    e.IDemp,
    e.nombreEMP,
    e.apellido,
    r.NombreRol,
    s.Sucursal
FROM usuarios_empleado u
INNER JOIN Empleado e ON u.IDemp = e.IDemp
LEFT JOIN roles r ON e.IDRol = r.IDRol
LEFT JOIN sucursal s ON e.idSucursal = s.idSucursal;
GO

INSERT INTO roles (NombreRol) VALUES ('Jefe'), ('Administrador'), ('Cajero');

INSERT INTO sucursal (idSucursal, Sucursal, numerotelefono) VALUES
(1, 'San Miguel Centro', '26601122'),
(2, 'La Union Sucursal', '26043344');

INSERT INTO categorias (NombreCategoria) VALUES
('Almacenamiento'),
('Perifericos'),
('Componentes');

INSERT INTO marcas (NombreMarca) VALUES
('Kingston'),
('Logitech'),
('ASUS');

INSERT INTO Empleado (IDemp, nombreEMP, apellido, Rol, IDRol, idSucursal) VALUES
(1, 'Kevin', 'Hernandez', 'Jefe', 1, 1),
(2, 'Misael', 'Quintanilla', 'Administrador', 2, 1),
(3, 'Amilcar', 'Iglesias', 'Cajero', 3, 2);

INSERT INTO usuarios_empleado (IDemp, Usuario, Clave, Activo) VALUES
(1, 'jefe_sm', '1234', 1),
(2, 'admin_sm', '1234', 1),
(3, 'cajero_lu', '1234', 1);

INSERT INTO productos (IDprod, nombreProd, costoprod, existencias, descripcion, IDCategoria, IDMarca) VALUES
(1, 'SSD NVMe 1TB', 68.00, 15, 'Unidad M.2 PCIe', 1, 1),
(2, 'Mouse G203 Lightsync', 24.50, 25, 'Mouse gamer 8000 DPI', 2, 2);

INSERT INTO servicios (NombreServicio, CostoServicio, Descripcion) VALUES
('Mantenimiento preventivo', 20.00, 'Limpieza interna y cambio de pasta termica'),
('Diagnostico de equipo', 10.00, 'Revision de hardware y fallas del sistema');

INSERT INTO cliente (DUIcl, Nombre, Apellido, telefono, direccion, correo) VALUES
(123456789, 'Ana', 'Lopez', '7788-9900', 'San Miguel', 'ana.lopez@correo.com');
GO