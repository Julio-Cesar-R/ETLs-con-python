# Libreria para obtener datos json y datetime para crear intervalos de repeticion
import requests, datetime

# Libreria prefect, tareas y flujos
from prefect import task, Flow

# Creacion de intervalos de tiempo
from prefect.schedules import IntervalSchedule

# Atrapar datos json y generar archivos json
import json

# EXTRACT
# task con log, reintentos, tiempo entre reintentos
@task(log_stdout=True, max_retries=3, retry_delay=datetime.timedelta(minutes=1))
def extract():
    print("Obetenemos la respuesta de la api")
    raw = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    print(f"El codigo de espuesta de la api es {raw.status_code}")
    # Genera una respuesta json
    raw = json.loads(raw.text)
    # Crear archivo jsnon
    with open(".\\raw.json", "w", encoding="utf-8") as file:
        json.dump(raw, file, ensure_ascii=False, indent=4)

    return raw


# TRANSFORM
@task(log_stdout=True)
def tranform(raw):
    print("Ejecutando la tranformacion")
    transformed = raw["title"]

    with open(".\\transformed.json", "w", encoding="utf-8") as file:
        json.dump(transformed, file, ensure_ascii=False, indent=4)
    return transformed


# LOAD
@task(log_stdout=True)
def load(transformed):

    print("*****")
    print("titulo del primero objeto")
    print(str(transformed))


# Ejecucion del flujo en intervalos de un minuto
schedule = IntervalSchedule(interval=datetime.timedelta(minutes=1))

# Flujo que ejecuta las tasks
with Flow("p.3 jasonplaceholder", schedule) as flow:
    raw = extract()
    transformed = tranform(raw)
    load(transformed)
# Ejecuta el flujo
flow.run()
