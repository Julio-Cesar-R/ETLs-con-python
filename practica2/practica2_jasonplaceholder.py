import requests
from prefect import task, Flow

@task
def extract():
    response=requests.get("https://jsonplaceholder.typicode.com/posts")
    response=response.json()
    return response
@task
def load(response):
    for index in range(len((response))):
        id_libro= response[index]["id"]
        titulo= response[index]["title"]
        print(str(id_libro),str(titulo))
        

    '''
    output=response[0]["title"]
    print("*****")
    print("titutlo del primero objeto")
    print(str(output))
'''
with Flow("p.2 jasonplaceholder") as flow:
    raw=extract()
    load(raw)

flow.run()

