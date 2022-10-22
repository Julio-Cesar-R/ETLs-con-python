# Libreria para obtener datos json y datetime para crear intervalos de repeticion
import requests, datetime

# Libreria prefect, tareas y flujos
from prefect import task, Flow

# Atrapar datos json y generar archivos json
import json

# EXTRACT
# task con log, reintentos, tiempo entre reintentos
@task(log_stdout=True, max_retries=3, retry_delay=datetime.timedelta(minutes=1))
def extract():
    print("Obetenemos la respuesta de la API")
    raw = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    print(f"El codigo de espuesta de la api es {raw.status_code}")
    # Genera una respuesta json
    raw = json.loads(raw.text)

    return raw


# TRANSFORM
@task(log_stdout=True)
def tranform(raw):
    print("Ejecutando la tranformacion")
    transformed = raw["title"]

    return transformed


# LOAD
@task(log_stdout=True)
def load(transformed):

    print("*****")
    print("titulo del primero objeto")
    print(str(transformed))


# Flujo que ejecuta las tasks
with Flow("p.3 jasonplaceholder") as flow:
    raw = extract()
    transformed = tranform(raw)
    load(transformed)
# Subir el flujo a prefect cloud
flow.register(project_name="practica4jsonplaceholder")
