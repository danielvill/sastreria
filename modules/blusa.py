# Medidas de Blusa
#Largo de Blusa
#Cort Pecho
#Cort Cintura
#Largo de Manga
#Puño
#Cuello
class Blusa:
    def __init__(self,id_cliente,largo_blusa,pecho,cintura,manga,puño,cuello):
        
        self.id_cliente=id_cliente
        self.largo_blusa=largo_blusa
        self.pecho=pecho
        self.cintura=cintura
        self.manga=manga
        self.puño=puño
        self.cuello=cuello
        
        
    def BlusaDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "largo_blusa" : self.largo_blusa,
            "pecho": self.pecho,
            "cintura": self.cintura,
            "manga": self.manga,
            "puño": self.puño,
            "cuello": self.cuello
        }