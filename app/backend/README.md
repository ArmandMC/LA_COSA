# Proyecto LaCosa

Este proyecto utiliza FastAPI y Uvicorn para crear una API web de alto rendimiento.

## Estructura del Proyecto

api.py: Contiene las rutas y endpoints de la API.

constants.py: Contiene alguans constantes de la aplicacion.

main.py: Archivo principal que se utiliza para iniciar la aplicación.

settings.py: Contiene las configuraciones principales, como variables de entorno.

version.py: version actual de la aplicación.

game/models/db.py: Contiene la instancia de la base de datos.

game/*/endpoints.py: Contiene los endpoints de la clase *.

game/*/models.py: Contiene los modelos de clase * de la base de datos usando PonyORM.

game/*/schemas.py: Contiene esquemas y modelos de Pydantic de la clase *.

game/*/utils.py: Funciones auxiliares y utilidades generales para la clase *.

.gitignore: Archivo que especifica qué archivos y directorios deben ser ignorados por Git.

README.md: Documentación del proyecto.

requirements.txt: Lista de dependencias del proyecto.

alembic.ini: Configuración de Alembic, en caso de que se utilice para migraciones de base de datos.

prestart.sh: Script opcional que puede ser ejecutado antes de iniciar la aplicación para realizar tareas previas.


## Ejecucion del proyecto

### Virtual environment:
Primero hay que crear un virtual environment y instalar las dependencias.

Linux:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

### Levantar el servidor:
Para ejecutar el proyecto, debes ejecutar el siguiente comando en la raíz del proyecto:

```bash
uvicorn main:app --reload
```

El comando anterior ejecutará la aplicación y la reiniciará automáticamente cada vez que se realice un cambio en el código fuente.

Para acceder a la documentación de la API, debes abrir tu navegador en la siguiente dirección:

Swagger UI:

URL: http://localhost:8000/docs
Swagger UI te proporciona una interfaz interactiva donde puedes ver todos tus endpoints, los detalles de los parámetros, las respuestas y también probar los endpoints directamente desde el navegador.

ReDoc:

URL: http://localhost:8000/redoc
ReDoc es otra herramienta que proporciona una documentación visualmente agradable y está basada en la especificación OpenAPI generada por FastAPI.

Nota: El puerto 8000 es el puerto predeterminado cuando inicias tu aplicación con Uvicorn. Si estás usando un puerto diferente, asegúrate de cambiar el número de puerto en las URLs mencionadas anteriormente.

## Ejecutar test
Para ejecutar los test desde windows hay que tener instalado make, que se puede instalar con chocolatey.
```
$ choco install make
```

### Test unitario
Para ejecutar los test unitarios hay que ejecutar el siguiente comando en la carpeta tests:
```
$ make
```

### Test de integración
Para ejecutar los test de integración hay que ejecutar el siguiente comando en la carpeta tests:
```
$ make run_integration_tests
```

### test end to end
Antes de ejecutar los test end to end hay que tener levantado el servidor con el siguiente comando:

Linux:
```
export ENVIRONMENT=test
uvicorn main:app
```

Windows:
```
set ENVIRONMENT=test
uvicorn main:app
```

Y luego ejecutar los test end to end en otra terminal con el siguiente comando en la carpeta tests:
Linux:
```
$ make l_run_end2end_tests
```

Windows:
```
$ make w_run_end2end_tests
```