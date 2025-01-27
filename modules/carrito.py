class Carrito:
    def __init__(self,id_cliente,id_producto,producto,cantidad,precio  ):
        
        self.id_cliente = id_cliente
        self.id_producto=id_producto
        self.producto=producto # Este es el nombre de producto
        self.cantidad=cantidad
        self.precio=precio
        
        
    def CarritoDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "id_producto": self.id_producto,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            
        }