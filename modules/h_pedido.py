class H_pedido:
    def __init__(self,id_pedido,id_cliente,id_producto,producto,cantidad,precio ,resultado,fecha_entrega,estado  ):
        
        self.id_pedido=id_pedido
        self.id_cliente=id_cliente
        self.id_producto=id_producto
        self.producto=producto
        self.cantidad=cantidad
        self.precio=precio
        self.resultado=resultado
        self.fecha_entrega=fecha_entrega
        self.estado=estado
        
        

    def HpedidoDBCollection(self):
        return{
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "id_producto": self.id_producto,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "resultado": self.resultado,
            "fecha_entrega": self.fecha_entrega,
            "estado": self.estado,
            
        }
    