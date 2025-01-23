class Producto:
    def __init__(self,id_producto,nombre,precio,categoria,subcategoria,descripcion,imagen):
        
        self.id_producto=id_producto
        self.nombre=nombre
        self.precio=precio
        self.categoria=categoria
        self.subcategoria=subcategoria
        self.descripcion=descripcion
        self.imagen=imagen
        
    def ProductoDBCollection(self):
        return{
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "subcategoria": self.subcategoria,
            "descripcion": self.descripcion,
            "imagen": self.imagen
        }