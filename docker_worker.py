import docker


dC = docker.DockerClient(base_url='unix://var/run/docker.sock', version="auto", timeout=60)
BASE_IMAGE = 'mariosky/evo_worker:latest'


def create_worker(env, command):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(env, command=command)
    start(container)
    return container


class ContainerException(Exception):
    """
    There was some problem generating or launching a docker container
    for the user
    """
    pass


class ImageException(Exception):
    """
    There was some problem reading image
    """
    pass



def make_container(env, command = "python /home/EvoWorker/ga_worker.py %s " ):
    return dC.containers.create(BASE_IMAGE, environment=env ,command=command,  labels={'evo_worker':'ga' })


def start(cont):
    dC.start(cont['Id'])



def kill_all():
    for container in get_containers('evo_worker'):
        print "Killing: ", container
        container.kill()


def remove_all():
    for container in get_containers(all=True):
        print "Removing: ", container
        container.remove(force=True)


def get_containers(label='evo_worker', all=False):
    return dC.containers.list(all=all, filters={'label': label})


