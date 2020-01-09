from flask import Blueprint, request
from flask_api import status
from elastic import contribuyente as es_con
from oracle_util.oracle_util import execute_consulta
import re

blueprint = Blueprint(name='contribuyente', import_name=__name__)


@blueprint.route(
    rule='/<int:cuit>/<string:id_ficha>',
    methods=['GET'],
    strict_slashes=False)
def profile(cuit: int, id_ficha: int):
    if request.method == 'GET':
        return get_profile(cuit, id_ficha)


def get_hipotesis(cuit: int, id_ficha: int):
    print("buscando hipotesis con ficha "+str(id_ficha))
    reg = execute_consulta(""" select ID_HIPOTESIS,ID_CORRIDA 
                                from fiscar.PASAJES_LOTES_CONTRIB_DET 
                                where N_LOTE={id_ficha} 
                                  and N_CUIT = {cuit} 
                           """.format(id_ficha=id_ficha, cuit=cuit))
    return reg


def get_profile(cuit: int, id_ficha: int):  
    x = re.search(r"[0-9]{1,9}", id_ficha)
    idLote = x.group()
    if idLote is not None:
        reg = get_hipotesis(cuit, idLote)
        print(reg)
        if reg is not None:
            id_hipotesis = reg[0]
            id_corrida = reg[1]
            print("buscando doc para hipotesis ",str(id_hipotesis)," corrida ",str(id_corrida))
            response = es_con.get_contribuyente_by_cuit_idmatriz(cuit,
                                                                 id_hipotesis,
                                                                 id_corrida)
            if not response:
                return '', status.HTTP_404_NOT_FOUND
            return (response['hits']['hits'][0]['_source'])
        else:
           return '', status.HTTP_404_NOT_FOUND     