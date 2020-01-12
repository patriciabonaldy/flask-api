from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pdfkit
import os


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
                                                    "evidencia_caso":{
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
                                                    
                                                    },
                                                    {"id_corrida": "830", 
                                                "fecha_corrida": "01/02/2020", 
                                                "periodo_desde": "199801", 
                                                "periodo_hasta": "202002", 
                                                "tipo_periodo_vto": "M",
                                                "evidencia_caso":{
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
                                                    "id_corrida": "831", 
                                                    "fecha_corrida": "01/02/2020", 
                                                    "periodo_desde": "199801", 
                                                    "periodo_hasta": "202002", 
                                                    "tipo_periodo_vto": "M",
                                                    "evidencia_caso": {
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

    def create_html(self):
        template = self.tpl_env.get_template("index2.html")        
        return template.render(data=self.df)


    def create_pdf(self):
      __file__ = os.getcwd()
      file_html =os.path.join(__file__,"resources", "ficha.html")
      filename =os.path.join(__file__,"resources", "ficha.pdf")

      if os.path.exists(file_html):
        os.remove(file_html)
        
      f= open(file_html,"w+")
      html = self.create_html()
      f.write(html)
      f.close()
      config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
      pdfkit.from_url(file_html, filename, configuration=config)

        
   
