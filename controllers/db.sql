create table cliente(
    id _cliente int primary key auto_increment,
    nombre varchar(50),
    apellido varchar(50),
    telefono varchar(50),
    correo varchar(50),
    contraseña  varchar(50)
)

create table producto(
    id_producto int primary key auto_increment,
    nombre varchar(50),
    precio decimal(10, 2),
    categoria varchar(50),
    descripcion varchar(50),
    imagen varchar(50),
)

create table pedido(
    id_pedido int primary key auto_increment,
    id_cliente int,
    fecha_pedido date,
    estado_pedido varchar(50),-- esto se refiere si esta pendiente 
    productos varchar(50),-- esto necesito especificar que tipo de medidas son osea cuanto de mano izquierda cuanto de mano derecha a eso me refiero
    precio decimal(10, 2),
)

create table h_pedido(
    id_pedido int primary key auto_increment,
    id_cliente int,
    fecha_pedido date,
    fecha_entrega date,
    estado_pedido varchar(50),-- esto se refiere si esta pendiente 
    productos varchar(50),-- esto necesito especificar que tipo de medidas son osea cuanto de mano izquierda cuanto de mano derecha a eso me refiero
    precio decimal(10, 2),
)
