# Medidas de Chaleco
#Chaleco
#Largo
#Cadera
#Escote

class Chaleco:
    def __init__(self,id_cliente,largo,cadera,escote):
        
        self.id_cliente=id_cliente
        self.largo=largo
        self.cadera=cadera
        self.escote=escote
        
        
    def ChalecoDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "largo" : self.largo,
            "cadera": self.cadera,
            "escote": self.escote
            
            
        }