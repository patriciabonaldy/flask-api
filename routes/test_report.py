from flask import Blueprint, request
from flask_api import status

from report.ficha_contribuyente import PdfTest

blueprint = Blueprint(name='test_report', import_name=__name__)


@blueprint.route(
    rule='/',
    methods=['GET'],
    strict_slashes=False)
def test():
    if request.method == 'GET':
        pdf_test = PdfTest()
        return pdf_test.create_pdf(), status.HTTP_200_OK
