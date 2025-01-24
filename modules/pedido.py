class Pedido:
    def __init__(self,id_pedido,nombre,telefono,id_producto,producto,cantidad,precio ,resultado ):
        
        self.id_pedido=id_pedido
        self.nombre=nombre
        self.telefono=telefono
        self.id_producto=id_producto
        self.producto=producto
        self.cantidad=cantidad
        self.precio=precio
        self.resultado= resultado
        
        
    def PedidoDBCollection(self):
        return{
            "id_pedido": self.id_pedido,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "id_producto": self.id_producto,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "resultado": self.resultado,
        }