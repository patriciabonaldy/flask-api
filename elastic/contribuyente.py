from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def get_contribuyente_by_cuit_idmatriz(
        cuit: int,
        id_hipotesis: int,
        id_corrida: int):
    es = Elasticsearch(
        hosts=getenv("ELASTIC_IPS").split(","),
        port=9200,
        http_compress=True)
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"cuit": cuit}},
                    {"term": {"id_hipotesis": id_hipotesis}},
                    {"term": {"id_corrida": id_hipotesis}}
                ]
            }
        }
    }
    response = es.search(
        index="contribuyente",
        body=query,
        filter_path=['hits.hits._source']
    )
    return response
