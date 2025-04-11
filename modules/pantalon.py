# Medidas para pantalon
#
#Alto de Rodilla
#Largo de Pantalo
#Cont De Cintura
#Cort de Cadera
#Muslo
#Rodilla
#Basta
#Tiro

class Pantalon:
    def __init__(self,id_cliente,alto_rodilla,largo_pantalon,cintura,cadera,muslo,rodilla,basta,tiro):
        
        self.id_cliente=id_cliente
        self.alto_rodilla=alto_rodilla
        self.largo_pantalon=largo_pantalon
        self.cintura=cintura
        self.cadera=cadera
        self.muslo=muslo
        self.rodilla=rodilla
        self.basta=basta
        self.tiro=tiro
        
        
    def PantalonDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "alto_rodilla" : self.alto_rodilla,
            "largo_pantalon": self.largo_pantalon,
            "cintura": self.cintura,
            "cadera": self.cadera,
            "muslo": self.muslo,
            "rodilla": self.rodilla,
            "basta": self.basta,
            "tiro": self.tiro
            
        }