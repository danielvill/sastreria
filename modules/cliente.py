class Cliente:
    def __init__(self,id_cliente,nombre,apellido,telefono,correo,contraseña):
        
        self.id_cliente=id_cliente
        self.nombre=nombre
        self.apellido=apellido
        self.telefono=telefono
        self.correo=correo
        self.contraseña=contraseña
        
    def ClienteDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "correo": self.correo,
            "contraseña": self.contraseña
        }