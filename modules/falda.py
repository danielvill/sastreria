#Falda
#Alto de Cadera
#Largo de Cadera
#Cort De Cintura
#Cont De Cadera
#Ancho de Vuelo



class Falda:
    def __init__(self,id_cliente,largo_cadera,cintura,cadera,vuelo):
        
        self.id_cliente=id_cliente
        self.largo_cadera=largo_cadera
        self.cintura=cintura
        self.cadera=cadera
        self.vuelo=vuelo
        
        
    def FaldaDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "largo_cadera" : self.largo_cadera,
            "cintura": self.cintura,
            "cadera": self.cadera,
            "vuelo": self.vuelo
            
            
            
        }