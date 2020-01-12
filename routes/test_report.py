from flask import Blueprint, request, send_file
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
        #return pdf_test.create_pdf(), status.HTTP_200_OK
        file_path = pdf_test.create_pdf()
        return send_file(file_path, as_attachment=True)
