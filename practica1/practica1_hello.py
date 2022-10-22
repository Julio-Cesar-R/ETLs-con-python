from prefect import task, Flow


@task
def load():
    print("hello wolrd")


with Flow("p1.1 hello world") as flow:
    load()

flow.run()
