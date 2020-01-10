#!/bin/bash

APP_NAME=fisca-data-profile-api
VERSION=$(git describe --tags)

if [ -z $VERSION ]; then
    VERSION=0.0.1 #Por si no hay version en git aun
fi


create_env(){
pipenv --python 3.7
pipenv install
pipenv install --dev
exit
echo "Para activar el nuevo env basta con hacer pipenv shell"
}

run_dev(){
    export FLASK_ENV=development
    export FLASK_APP=app.py
    flask run --host=0.0.0.0 --port 5000
}

create_docker(){
    docker images | grep $APP_NAME | awk '{print $3}' | xargs docker rmi -f
    docker build -t $APP_NAME:$VERSION .
    docker tag $APP_NAME:$VERSION $APP_NAME:latest
    echo "Ya puede iniciar el container con docker-compose up -d"
}

release(){
    rm -fr dist/*
    mkdir -p dist    

    if [ $? -ne 0 ]; then
        echo "El comando fallo"
        echo "Posibles problemas:"
        echo "1 - No haber taggeado en git"
        exit 1
    fi
    
    docker image ls $APP_NAME:$VERSION | grep $APP_NAME

    if [ $? -ne 0 ]; then
        echo "El comando fallo"
        echo "Posibles problemas:"
        echo "1 - No haber creado la imagen docker (corra pipenv run build-docker)"
        echo "2 - Que la tag de la imagen docker y la ultima tag de proyecto no coincidan"
        exit 1
    fi

    docker save $APP_NAME:$VERSION | gzip -c > dist/image.tar.gz
    tar cvzf dist/$APP_NAME-$VERSION.tar.gz dist/image.tar.gz ./docker-compose.release.yml

    if [ $? -ne 0 ]; then
        echo "El comando fallo"
        exit 1
    fi

    echo "Se creo la release dist/$APP_NAME-$VERSION.tar.gz"
    md5sum dist/$APP_NAME-$VERSION.tar.gz | awk '{print $1}' > dist/$APP_NAME-$VERSION.tar.gz.md5
    sha1sum dist/$APP_NAME-$VERSION.tar.gz | awk '{print $1}' > dist/$APP_NAME-$VERSION.tar.gz.sha1
    echo "Usuario sua: "
    read username
    echo "Password sua: "
    read password
    curl --noproxy '*' -v -k -u "$username:$password" --upload-file dist/$APP_NAME-$VERSION.tar.gz "https://nexus.cloudint.afip.gob.ar/nexus/repository/fisca-seleccion-casos-raw/$APP_NAME/$VERSION/$APP_NAME-$VERSION.tar.gz"
    curl --noproxy '*' -v -k -u "$username:$password" --upload-file dist/$APP_NAME-$VERSION.tar.gz.md5 "https://nexus.cloudint.afip.gob.ar/nexus/repository/fisca-seleccion-casos-raw/$APP_NAME/$VERSION/$APP_NAME-$VERSION.tar.gz.md5"
    curl --noproxy '*' -v -k -u "$username:$password" --upload-file dist/$APP_NAME-$VERSION.tar.gz.sha1 "https://nexus.cloudint.afip.gob.ar/nexus/repository/fisca-seleccion-casos-raw/$APP_NAME/$VERSION/$APP_NAME-$VERSION.tar.gz.sha1"
    echo "Release: https://nexus.cloudint.afip.gob.ar/nexus/repository/fisca-seleccion-casos-raw/$APP_NAME/$VERSION/$APP_NAME-$VERSION.tar.gz"

    rm -fr dist/*
}


test(){
    #TODO: Crear tests para correr XD
    echo ""
}

case "$1" in
    env)
        create_env
        ;;
    docker)
        create_docker
        ;;
    rundev)
        run_dev
        ;;
    release)
        release
        ;;
    *)
        echo "Usage: $0 {env|docker|rundev|release}"
esac