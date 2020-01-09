from flask_api import FlaskAPI, status
import logging
from routes import contribuyente, test, test_report

app = FlaskAPI(__name__)

logging.basicConfig(filename="./log/app.log")

app.register_blueprint(contribuyente.blueprint,
                       url_prefix="/profile/api/v1/contribuyente")
app.register_blueprint(test.blueprint,
                       url_prefix="/profile/api/v1/test")

app.register_blueprint(test_report.blueprint,
                       url_prefix="/profile/api/v1/test_report")


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    app.logger.info(error)
    return ('', status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    app.run()
