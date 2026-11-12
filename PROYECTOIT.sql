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

Create table productos(
IDprod int not null primary key,
nombreProd Varchar(30) not null,
costoprod decimal(10,2) not null,
existencias int not null,
descripcion varchar(50)
)
insert into productos values(1, "Nvidia RTX 5070ti", 850, 7, "Targeta grafica de 16gb de vram")


Create table sucursal(
idSucursal int not null primary key,
Sucursal varchar(80) not null,
numerotelefono varchar(8) not null,
)

go

Create table Empleado(
IDemp int not null primary key,
nombreEMP varchar(30) not null,
apellido varchar(20) not null,
Rol varchar(20) not null,
)


--Alguien puede hacer las foreign key para referenciar los clientes, sucursal,empleado, producto
--Si hay mas ideas podemos agregar otra tabla para agregar mas servicios
--Como mantenimiento, reparacion etc etc.
Create table factura(
IDfact int not null identity(1,1) primary key ,
Sucursal int not null,
empleFACT int not null,
sucurFACT int not null,
prodFACT int not null,
ClienFACT int not null,
)
--No esta creada esta tabla de factura
--Hola