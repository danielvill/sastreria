class Pedido:
    def __init__(self,id_pedido,id_cliente,fecha_pedido,estado_pedido,productos,precio  ):
        
        self.id_pedido=id_pedido
        self.id_cliente=id_cliente
        self.fecha_pedido=fecha_pedido
        self.estado_pedido=estado_pedido
        self.productos=productos
        self.precio=precio

        
    def PedidoDBCollection(self):
        return{
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "fecha_pedido": self.fecha_pedido,
            "estado_pedido": self.estado_pedido,
            "productos": self.productos,
            "precio": self.precio
        }