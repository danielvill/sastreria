class Medida:
    def __init__(self,id_medida,id_cliente,espalda,busto,a_brazo,l_brazo,a_puño,t_espalda,t_delantero,l_pinza,cintura,l_falda,l_pierna,a_pierna,l_tiro,l_rodilla ):
        
        self.id_medida=id_medida
        self.id_cliente=id_cliente
        self.espalda=espalda
        self.busto=busto
        self.a_brazo=a_brazo
        self.l_brazo=l_brazo
        self.a_puño=a_puño
        self.t_espalda=t_espalda
        self.t_delantero=t_delantero
        self.l_pinza=l_pinza
        self.cintura=cintura
        self.l_falda=l_falda
        self.l_pierna=l_pierna
        self.a_pierna=a_pierna
        self.l_tiro=l_tiro
        self.l_rodilla=l_rodilla
        
        
        
    def MedidaDBCollection(self):
        return{
            "id_medida": self.id_medida,
            "id_cliente": self.id_cliente,
            "espalda": self.espalda,
            "busto": self.busto,
            "a_brazo": self.a_brazo,
            "l_brazo": self.l_brazo,
            "a_puño": self.a_puño,
            "t_espalda": self.t_espalda,
            "t_delantero": self.t_delantero,
            "l_pinza": self.l_pinza,
            "cintura": self.cintura,
            "l_falda": self.l_falda,
            "l_pierna": self.l_pierna,
            "a_pierna": self.a_pierna,
            "l_tiro": self.l_tiro,
            "l_rodilla": self.l_rodilla,

            
        }