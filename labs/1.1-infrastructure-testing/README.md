# Terratest test

## Requisitos previos

1. Disponer de [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Haber configurado los [credenciales de AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
3. Obtener el nombre de usuario de AWS:

    ```sh
    AWS_USERNAME=$(aws sts get-caller-identity | jq -r '.Arn' | cut -d '/' -f2)
    ```

4. Comprobar el nombre de usuario obtenido en el comando anterior:

    ```sh
    echo "AWS_USERNAME: ${AWS_USERNAME}"
    ```

    El resultado del comando anterior debería ser algo como lo siguiente:

    ```sh
    AWS_USERNAME: xoanmm
    ```

5. Crear una variable para el nombre del bucket con el usuario en este, que siga el formato `terratest-test-<aws_username>`

    ```sh
    AWS_S3_BUCKET_NAME="terratest-test-${AWS_USERNAME}"
    ```

6. Comprobar el nombre del bucket obtenido en el comando anterior:

    ```sh
    echo "AWS_S3_BUCKET_NAME: ${AWS_S3_BUCKET_NAME}"
    ```

    El resultado del comando anterior debería ser algo similar a lo siguiente:

    ```sh
    AWS_S3_BUCKET_NAME: terratest-test-xoanmm
    ```

7. [Go](https://go.dev/) versión >=1.21.1
   - Para su instalación se recomienda seguir los pasos de la [página oficial](https://go.dev/doc/install)

8. [Terraform](https://developer.hashicorp.com/terraform) version >=1.5.0
   - Para su instalación se recomienda utilizar la herramienta [tfenv](https://github.com/tfutils/tfenv)

## Laboratorio terratest

1. Crear un bucket para almacenar el tfstate con el nombre almacenado en la variable `AWS_S3_BUCKET_NAME`:

    ```sh
    aws s3api create-bucket --bucket "${AWS_S3_BUCKET_NAME}" --region "eu-central-1" --create-bucket-configuration LocationConstraint="eu-central-1"
    ```

    El resultado del comando anterior debería ser algo como lo siguiente:

    ```json
    {
        "Location": "http://terratest-test-xoanmm.s3.amazonaws.com/"
    }
    ```

2. Moverse al directorio `src`:

    ```sh
    cd src
    ```

3. Realizar el terraform init pasando por línea de comandos la configuración del bucket para almacenar el tfstate:

    ```sh
    terraform init -reconfigure '-backend-config=key=eu-central-1/terratest-test.tfstate' '-backend-config=bucket=<AWS_S3_BUCKET_NAME>' '-backend-config=region=eu-central-1'
    ```

4. Realizar un plan pasando como variable `username` el nombre el usuario de AWS obtenido en pasos anteriores:

    ```sh
    terraform plan -var username="${AWS_USERNAME}" -out "terraform-${AWS_USERNAME}.plan"
    ```

5. Realizar un apply para comprobar el output que se generara como el nombre del bucket:

    ```sh
    terraform apply "terraform-${AWS_USERNAME}.plan"
    ```

6. Comprobar el output `bucket_name`:

    ```sh
    terraform output bucket_name
    ```

    El resultado del comando anterior debería ser algo como lo siguiente:

    ```sh
    "terratest-lab-xoanmm"
    ```

7. Destruir los recursos creados:

    ```sh
    terraform apply -destroy -var username="${AWS_USERNAME}" -auto-approve
    ```

8. Moverse al directorio `test`:

    ```sh
    cd ./test
    ```

9. Descargar las dependencias necesarias:

    ```sh
    go mod tidy
    ```

10. Actualizar la [línea 14 del fichero ./test/basic_example_test.go](./test/basic_example_test.go#L14) el valor de `username` con el nombre del usuario de aws

    > Es posible comprobar el nombre del usuario ejecutando el comando `echo $AWS_USERNAME` en la misma terminal en la que se hayan ejecutado los comando anteriores

11. Actualizar la [línea 15 del fichero ./test/basic_example_test.go](./test/basic_example_test.go#L15) el valor de `backendConfigBucket` con el nombre del bucket donde se almacenará el tfstate para el usuario

    > Es posible comprobar el nombre del usuario ejecutando el comando `echo $AWS_S3_BUCKET_NAME` en la misma terminal en la que se hayan ejecutado los comando anteriores

12. Ejecutar los tests con terratest:

    ```sh
    go test -v -timeout 30m
    ```

## Limpieza de recursos

1. Eliminar el contenido y el creado para almacenar los ficheros tfstate creados durante el laboratorio:

    ```sh
    aws s3 rm "s3://${AWS_S3_BUCKET_NAME}" --recursive
    aws s3api delete-bucket --bucket "${AWS_S3_BUCKET_NAME}"
    ```
