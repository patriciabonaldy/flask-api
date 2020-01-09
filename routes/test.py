from flask import Blueprint, request
from flask_api import status

blueprint = Blueprint(name='test', import_name=__name__)


@blueprint.route(
    rule='/',
    methods=['GET'],
    strict_slashes=False)
def test():
    if request.method == 'GET':
        return 'ok', status.HTTP_200_OK
