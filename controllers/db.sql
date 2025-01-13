create table cliente(
    id _cliente int primary key auto_increment,
    nombre varchar(50),
    apellido varchar(50),
    telefono varchar(50),
    correo varchar(50),
)

create table producto(
    id_producto int primary key auto_increment,
    nombre varchar(50),
    precio decimal(10, 2),
    categoria varchar(50),
    cantidad int,
    descripcion varchar(50),
    imagen varchar(50),
)

create table pedido(
    
)

