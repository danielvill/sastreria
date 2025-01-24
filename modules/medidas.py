class Medida:
    def __init__(self,id_medida,id_cliente,busto,cintura,cadera,espalda,mangas ,comentario ):
        
        self.id_medida=id_medida
        self.id_cliente=id_cliente
        self.busto=busto
        self.cintura=cintura
        self.cadera=cadera
        self.espalda=espalda
        self.mangas=mangas
        self.comentario=comentario
        

        
    def MedidaDBCollection(self):
        return{
            "id_medida": self.id_medida,
            "id_cliente": self.id_cliente,
            "busto": self.busto,
            "cintura": self.cintura,
            "cadera": self.cadera,
            "espalda": self.espalda,
            "mangas": self.mangas,
            "comentario": self.comentario
            
        }