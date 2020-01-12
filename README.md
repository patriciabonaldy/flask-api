# Fisca Data Profile API

## Development
https://www.valentinog.com/blog/python-pdf/
https://www.anomaly.net.au/blog/convert-html-and-css-to-pdfs-using-weasyprint-within-your-python-app/
https://pbpython.com/pdf-reports.html
https://pypi.org/project/pdfkit/
https://www.geeksforgeeks.org/python-convert-html-pdf/

Environment setup:
~~~bash
pipenv --python 3.7 && pipenv shell && pipenv install && pipenv install --dev
~~~

Para iniciar el servicio:

~~~bash
pipenv run dev
~~~

Crear un archivo dotenv con las siguientes variables:

- .env

~~~config
ELASTIC_IPS=10.30.205.62,10.30.205.66,10.30.205.84
ELASTIC_PORT=9200
~~~

## Deployment

### Creacion de virtual en Openstack

1. Se crea una virtual del tipo CPU2RAM3072HD10GB con la imagen RHEL7.6-V1.31

2. Instalar docker-ce, docker-compose, nginx y sus dependencias (se necesita tener configurado el proxy con salida a internet para este paso):

~~~bash
sudo yum install -y epel-release
sudo yum install -y device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y http://mirror.centos.org/centos/7/extras/x86_64/Packages/container-selinux-2.107-3.el7.noarch.rpm
sudo yum install -y docker-ce docker-ce-cli containerd.io nginx
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
~~~

3. Iniciar los servicios

~~~bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl start nginx
sudo systemctl enable nginx
~~~

4. Instalacion de la aplicacion

~~~bash
wget https://nexus.cloudint.afip.gob.ar/nexus/repository/fisca-seleccion-casos-raw/fisca-data-profile-api/<version>/fisca-data-profile-api-<version>.tar.gz
tar xfvz fisca-data-profile-api-<version>.tar.gz
sudo docker load -i image.tar.gz
sudo docker tag fisca-data-profile-api:<version> fisca-data-profile-api:latest
~~~

5. Limpiamos

~~~bash
rm -fr fisca-data-profile-api-<version>.tar.gz
rm -fr dist
~~~

6. Certificados

Creamos el directorio:

~~~bash
sudo mkdir -p /afip/trustore/certs/
~~~

En el caso de desarrollo/homologacion creamos certificados autofirmados:

~~~bash
sudo openssl req -x509 -nodes -days 999999 -newkey rsa:2048 -keyout /afip/trustore/certs/afip.key -out /afip/trustore/certs/afip.crt
sudo openssl dhparam -out /afip/trustore/certs/afip.pem 2048
~~~

En el caso de produccion, solo basta con ponerlos en el directorio que quieran

7. Configuracion de nginx

- /etc/nginx/conf.d/afip.conf:

~~~config
server {
    listen 443 http2 ssl;
    listen [::]:443 http2 ssl;

    server_name fisca-data-profile.cloudhomo.afip.gob.ar;

    ssl_certificate /afip/trustore/certs/afip.crt;
    ssl_certificate_key /afip/trustore/certs/afip.key;
    ssl_dhparam /afip/trustore/certs/afip.pem;

    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_buffering off;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
~~~

Activamos el redirect de http a https:

- /etc/nginx/default.d/ssl-redirect.conf:

~~~config
return 301 https://$host$request_uri/;
~~~

- Testeamos que la config este bien:

~~~bash
[appserv@fisca-data-profile /]sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
~~~

Si la respuesta es distinta entonces hay algo mal configurado. Revisar la linea que indique.


5. Levantamos los servicios
~~~bash
sudo docker-compose -f docker-compose.release.yml up -d
~~~

## Re-deploy

1. Bajar y borrar el container y su imagen

~~~bash
docker-compose -f docker-compose.release.yml down
sudo docker images -q | sudo xargs docker rmi -f
docker rmi fisca-data-profile-api:<version>
docker rmi fisca-data-profile-api:latest
~~~

2. Volver a crear y levantar el container

~~~bash
tar xfvz fisca-data-profile-api-<version>.tar.gz
sudo docker tag fisca-data-profile-api:<version> fisca-data-profile-api:latest
rm -fr dist
rm -fr fisca-data-profile-api-*.tar.gz
sudo docker-compose -f docker-compose.release.yml up -d
~~~

### Releasing

Se puede construir el release con el comando:

~~~bash
./service.sh docker
~~~

La imagen docker resultante se encuentra en el directorio **./dist**

A posterior, se puede subir el release a Nexus:

~~~bash
./service.sh release
~~~
