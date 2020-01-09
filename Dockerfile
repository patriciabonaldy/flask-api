FROM python:3.7.5-slim
LABEL maintainer="Matias Estevez <mestevez@afip.gob.ar>"

ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"
ENV PIP_CONFIG_FILE="/etc/pip.conf"


RUN mkdir /app
RUN mkdir /app/log
WORKDIR /app
COPY resources/pip.conf /etc/
COPY Pipfile .
COPY app.py .
COPY routes ./routes
COPY oracle ./oracle
COPY elastic ./elastic
RUN pip install pipenv --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout 500
RUN pipenv install
EXPOSE 5000
ENTRYPOINT ["pipenv", "run", "gunicorn", "--bind=0.0.0.0:5000","--workers","4","app:app"]
