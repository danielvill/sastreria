#Saco
#Talla Delantero
#Largo de Saco
#Ancho de espalda
#Largo de Manga
#Puño
#Ancho de Brazo
#Cont De Pecho
#Cont De Cintura
#Pecho
#Alto de Busto
#Distancia de Busto
#Talla de Espalda
#Media Espalda
#Escote


class Saco:
    def __init__(self,id_cliente,talla_dealntero,largo_saco,ancho_espalda,largo_manga,puño,ancho_brazo,cont_pecho,cont_cintura,pecho,alto_busto,distancia_busto,talla_espalda,media_espalda,escote):
        
        self.id_cliente=id_cliente
        self.talla_dealntero=talla_dealntero
        self.largo_saco=largo_saco
        self.ancho_espalda=ancho_espalda
        self.largo_manga=largo_manga
        self.puño=puño
        self.ancho_brazo=ancho_brazo
        self.cont_pecho=cont_pecho
        self.cont_cintura=cont_cintura
        self.pecho=pecho
        self.alto_busto=alto_busto
        self.distancia_busto=distancia_busto
        self.talla_espalda=talla_espalda
        self.media_espalda=media_espalda
        self.escote=escote
        
        
    def SacoDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "talla_dealntero" : self.talla_dealntero,
            "largo_saco": self.largo_saco,
            "ancho_espalda": self.ancho_espalda,
            "largo_manga": self.largo_manga,
            "puño": self.puño,
            "ancho_brazo": self.ancho_brazo,
            "cont_pecho": self.cont_pecho,
            "cont_cintura": self.cont_cintura,
            "pecho": self.pecho,
            "alto_busto": self.alto_busto,
            "distancia_busto": self.distancia_busto,
            "talla_espalda": self.talla_espalda,
            "media_espalda": self.media_espalda,
            "escote": self.escote
            
            
        }