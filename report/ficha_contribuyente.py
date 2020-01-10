from jinja2 import Environment, FileSystemLoader


class PdfTest:
    def __init__(self):
        self.tpl_dir = FileSystemLoader("templates")
        self.tpl_env = Environment(loader=self.tpl_dir)
        self.df = {"cuit": "20000000093", 
                   "nombre": "PEPITO",
                   "hipotesis": [{"id_hipotesis": "914", 
                                  "descripcion": "HIP SEGURO SOCIAL", 
                                  "dir_gral": "DGI", 
                                  "cod_instructivo": "MON-SESO-0001", 
                                  "id_impuesto": "431", 
                                  "tipo_desvio": "OTR", 
                                  "corridas": [{"id_corrida": "828", 
                                                "fecha_corrida": "01/02/2020", 
                                                "periodo_desde": "199801", 
                                                "periodo_hasta": "202002", 
                                                "tipo_periodo_vto": "M",
                                                "evidencia_caso": 
                                                {
                                                    "origen": "cruce_06", 
                                                    "select": 
                                                    [{ "nombre": "cuit", 
                                                       "columna": "cuit", 
                                                       "tipo": "string", 
                                                       "agregacion": "SUM", 
                                                       "valor": "1500"},
                                                     { "nombre": "remicoss", 
                                                       "columna": "remicoss", 
                                                       "tipo": "string", 
                                                       "agregacion": "SUM", 
                                                       "valor": "1500"},
                                                     { "nombre": "remicoss", 
                                                       "columna": "remicoss", 
                                                       "tipo": "string", 
                                                       "agregacion": "SUM", 
                                                       "valor": "1500"},
                                                     { "nombre": "MONTO", 
                                                       "columna": "MONTO", 
                                                       "tipo": "number", 
                                                       "agregacion": "SUM", 
                                                       "valor": "1500"}]
                                                       }},
                                                    {
                                                    "id_corrida": "829", 
                                                    "fecha_corrida": "01/02/2020", 
                                                    "periodo_desde": "199801", 
                                                    "periodo_hasta": "202002", 
                                                    "tipo_periodo_vto": "M",
                                                    "evidencia_caso": 
                                                    {
                                                        "origen": "cruce_06", 
                                                        "select": 
                                                        [{"nombre": "cuit",
                                                          "columna": "cuit", 
                                                          "tipo": "string", 
                                                          "agregacion": "SUM", 
                                                          "valor": "1500"},
                                                         {"nombre": "remicoss", 
                                                          "columna": "remicoss", 
                                                          "tipo": "string", 
                                                          "agregacion": "SUM", 
                                                          "valor": "1500"},
                                                         {"nombre": "remicoss", 
                                                          "columna": "remicoss", 
                                                          "tipo": "string", 
                                                          "agregacion": "SUM", 
                                                          "valor": "1500"},
                                                         {"nombre": "MONTO", 
                                                          "columna": "MONTO", 
                                                          "tipo": "number", 
                                                          "agregacion": "SUM", 
                                                          "valor": "1500"}]
                                                        }
                                                    
                                                    }]

                                  
                                  }]}

    def create_pdf(self):
        template = self.tpl_env.get_template("index2.html")        
        return template.render(data=self.df)
