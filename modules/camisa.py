#Camisa
#Largo de Camisa
#Ancho de espalda
#caida de hombro
#largo de manga
#puño
#ancho de brazo
#contorno de pecho
#contorno de cintura
#pecho
#cuello


class Camisa:
    def __init__(self,id_cliente,largo_camisa,ancho_espalda,caida_hombro,largo_manga,puño,ancho_brazo,contorno_pecho,cintura,pecho,cuello):
        
        self.id_cliente=id_cliente
        self.largo_camisa=largo_camisa
        self.ancho_espalda=ancho_espalda
        self.caida_hombro=caida_hombro
        self.largo_manga=largo_manga
        self.puño=puño
        self.ancho_brazo=ancho_brazo
        self.contorno_pecho=contorno_pecho
        self.cintura=cintura
        self.pecho=pecho
        self.cuello=cuello
        
        
    def CamisaDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "largo_camisa" : self.largo_camisa,
            "ancho_espalda": self.ancho_espalda,
            "caida_hombro": self.caida_hombro,
            "largo_manga": self.largo_manga,
            "puño": self.puño,
            "ancho_brazo": self.ancho_brazo,
            "contorno_pecho": self.contorno_pecho,
            "cintura": self.cintura,
            "pecho": self.pecho,
            "cuello": self.cuello
        }