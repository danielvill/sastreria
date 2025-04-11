#Medida de Leva
#Leva
#Talla de Espalda
#Largo de Saco
#Ancho de espalda
#Media Espalda
#Caida de Hombro
#Largo de Manga
#Ancho de Puño
#Ancho de Brazo
#Cont De Pecho
#Cont de Cintura
#Pecho
#Cuello

class Leva:
    def __init__(self,id_cliente,espalda,largo_saco,ancho_espalda,media_espalda,caida_hombro,largo_manga,ancho_puño,ancho_brazo,cont_pecho,cintura,pecho,cuello):
        
        self.id_cliente=id_cliente
        self.espalda=espalda
        self.largo_saco=largo_saco
        self.ancho_espalda=ancho_espalda
        self.media_espalda=media_espalda
        self.caida_hombro=caida_hombro
        self.largo_manga=largo_manga
        self.ancho_puño=ancho_puño
        self.ancho_brazo=ancho_brazo
        self.cont_pecho=cont_pecho
        self.cintura=cintura
        self.pecho=pecho
        self.cuello=cuello
        
        
    def LevaDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "espalda" : self.espalda,
            "largo_saco": self.largo_saco,
            "ancho_espalda": self.ancho_espalda,
            "media_espalda": self.media_espalda,
            "caida_hombro": self.caida_hombro,
            "largo_manga": self.largo_manga,
            "ancho_puño": self.ancho_puño,
            "ancho_brazo": self.ancho_brazo,
            "cont_pecho": self.cont_pecho,
            "cintura": self.cintura,
            "pecho": self.pecho,
            "cuello": self.cuello
            
            
            
            
        }