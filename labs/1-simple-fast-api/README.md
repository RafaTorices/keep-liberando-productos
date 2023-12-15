<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [simple-fast-api](#simple-fast-api)
  - [Descripcion](#descripcion)
  - [Software necesario](#software-necesario)
  - [Ejecución de código](#ejecución-de-código)
    - [Prerequisitos](#prerequisitos)
    - [Arrancar el servidor servidor](#arrancar-el-servidor-servidor)
      - [Arrancar el servidor a través de Python](#arrancar-el-servidor-a-través-de-python)
      - [Arrancar el servidor a través de docker-compose](#arrancar-el-servidor-a-través-de-docker-compose)
    - [Probar llamadas a los diferentes endpoints](#probar-llamadas-a-los-diferentes-endpoints)
    - [Ejecución de tests](#ejecución-de-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# simple-fast-api

## Descripcion

El objetivo de esta práctica es crear un ejemplo de servidor sencillo utilizando [fastapi](https://fastapi.tiangolo.com/)

## Software necesario

Es necesario disponer del siguiente software:

- `Python` en versión `3.8.5` o superior, disponible para los diferentes sistemas operativos en la [página oficial de descargas](https://www.python.org/downloads/release/python-385/)

- `virtualenv` para poder instalar las librerías necesarias de Python de forma aislada, es posible instalarlo a través del siguiente comando **una vez se haya instalado `Python`**:

    ```sh
    pip3 install virtualenv
    ```

- `docker` para poder crear contenedores, es posible instalarlo siguiendo la [guía de su página oficial](https://docs.docker.com/engine/install/)

- `docker-compose` para poder utilizar el fichero [docker-compose.yaml](./docker-compose.yaml) y crear los contenedores necesarios tanto para el servidor con [fastapi](https://fastapi.tiangolo.com/) como el contenedor para la base de datos de [MongoDB](https://www.mongodb.com/). Es posible instalarlo siguiendo la [guía de su página oficial](https://docs.docker.com/compose/install/).

## Ejecución de código

### Prerequisitos

1. Crear de virtualenv en la raíz del directorio para poder instalar las librerías necesarias:

    ```sh
    python3.8 -m venv venv
    ```

2. Activar el virtualenv creado en el directorio `venv` en el paso anterior:

    ```sh
    source venv/bin/activate
    ```

3. Librerías necesarias de Python, recogidas en el fichero `requirements.txt`, es posible instalarlas a través del siguiente comando:

    ```sh
    pip3 install -r requirements.txt
    ```

### Arrancar el servidor servidor

#### Arrancar el servidor a través de Python

1. Se utiliza una base de datos MongoDB como dependencia, por lo que en caso de no haberlo hecho es necesario levantar un contenedor Docker de Mongo para utilizar por parte del servidor:

    ```sh
    docker run --name mongo -d -e MONGODB_ROOT_PASSWORD=password -p 27017:27017 bitnami/mongodb:4.4.13-debian-10-r30
    ```

2. El servidor al arrancar buscará una variable de entorno llamada `MONGODB_URL` con la URL de acceso a mongo, por lo que es necesario exportar esta variable con la URL del mongo creado en el paso anterior:

    ```sh
    export MONGODB_URL="mongodb://root:password@localhost:27017"
    ```

3. Ejecutar el script utilizado para esperar hasta que mongo esté listo:

    ```sh
    ./tools/check_mongodb_is_ready.sh
    ```

4. Activar el virtualenv creado anteriormente, **sólo en caso de no estar ya activado**:

    ```sh
    source venv/bin/activate
    ```

5. Arrancar el servidor:

    ```sh
    python3 app.py
    ```

    **En caso de que en la primera ejecución el servidor falle mostrando un error con el mensaje `from fastapi import FastAPI ModuleNotFoundError: No module named 'fastapi'` será necesario desactivar y volver a activar el entorno virtual creado** ejecutando los siguientes comandos:

    ```sh
    deactivate
    source venv/bin/activate
    ```

#### Arrancar el servidor a través de docker-compose

1. Es posible arrancar el servidor y la dependencia que tiene con una BD de tipo MongoDB a través de contenedores `docker-compose`, para ello será necesario instalar esta herramienta en caso de no tenerlo ya instalada, siguiendo los pasos explicados en [la documentación oficial](https://docs.docker.com/compose/install/)

2. Una vez se tenga `docker-compose` instalado será posible arrancar los contenedores utilizando el fichero [docker-compose](docker-compose.yaml) del que se dispone en la raíz de la carpeta para este laboratorio, utilizando para ello el siguiente comando:

    ```sh
    docker-compose up -d
    ```

3. Es posible obtener los logs de los contenedores a través de los siguientes comandos:

    - Obtener logs del contenedor creado para la base de datos MongoDB:

        ```sh
        docker logs -f mongodb
        ```

    - Obtener logs del contenedor creado para el servidor `fast-api`:

        ```sh
        docker logs -f fast-api
        ```

### Probar llamadas a los diferentes endpoints

Una vez se haya arrancado el servidor de forma local o través de `docker-compose` es posible probar las diferentes peticiones a este:

- Probar una petición al endpoint `/`

    ```sh
    curl -X 'GET' \
    'http://0.0.0.0:8081/' \
    -H 'accept: application/json'
    ```

    Debería devolver la siguiente respuesta:

    ```json
    {"message":"Hello World"}
    ```

- Probar una petición al endpoint `/health`

    ```sh
    curl -X 'GET' \
    'http://0.0.0.0:8081/health' \
    -H 'accept: application/json'
    ```

    Debería devolver la siguiente respuesta.

    ```json
    {"health": "ok"}
    ```

### Ejecución de tests

**Para la ejecución de los tests de integración es necesario disponer de un MongoDB**, ese se proporcionará para los tests de igual forma que para la ejecución del servidor, por lo que es posible realizar los mismos pasos que para el MongoDB utilizado por la aplicación, creando un nuevo MongoDB:

```sh
docker run --name mongo -d -e MONGODB_ROOT_PASSWORD=password -p 27017:27017 bitnami/mongodb:4.4.13-debian-10-r30
```

Es necesario exportar la variable `MONGODB_URL` con la URL del Mongo a utilizar para los tests de integración:

```sh
export MONGODB_URL="mongodb://root:password@localhost:27017"
```

Es necesario indicar qué tests se quieren ejecutar, eligiendo en las siguientes opciones:

- Ejecución de todos los tests:

    ```sh
    pytest
    ```

- Ejecución únicamente de tests unitarios:

    ```sh
    pytest -m "not integtest"
    ```

- Ejecución únicamente de tests de integración:

    ```sh
    pytest -m "integtest"
    ```

- Ejecución de todos los tests y mostrar cobertura:

    ```sh
    pytest --cov
    ```

- Ejecución de únicamente de tests unitarios y mostrar cobertura:

    ```sh
    pytest -m "not integtest" --cov
    ```

- Ejecución de únicamente de tests de integración y mostrar cobertura:

    ```sh
    pytest -m "integtest" --cov
    ```

- Ejecución de todos los tests y generación de report de cobertura:

    ```sh
    pytest --cov --cov-report=html
    ```

- Ejecución únicamente de tests unitarios y generación de report de cobertura:

    ```sh
    pytest -m "not integtest" --cov --cov-report=html
    ```

- Ejecución únicamente de tests de integración y generación de report de cobertura:

    ```sh
    pytest -m "integtest" --cov --cov-report=html
    ```
