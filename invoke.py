# This will be used to prefix all docker objects (network, images, containers)
project_name = 'sflive-demo'
# This is the root domain where the app will be available
# The "frontend" container will receive all the traffic
root_domain = project_name + '.test'
# This is the host directory containing your PHP application
project_directory = '.'

# Usually, you should not edit the file above this point

docker_compose_files = [
    'docker-compose.yml',
]
services_to_build_first = [
    'php-base',
    'builder',
]
dinghy = False
power_shell = False
user_id = 1000
root_dir = '.'


def __extract_runtime_configuration(config):
    from invoke import run
    from sys import platform
    import os
    import sys
    from colorama import init, Fore
    init(autoreset=True)

    config['root_dir'] = os.path.dirname(os.path.abspath(__file__))

    try:
        docker_kernel = run('docker version --format "{{.Server.KernelVersion}}"', hide=True).stdout
    except:
        docker_kernel = ''

    if platform == "darwin" and docker_kernel.find('linuxkit') != -1:
        config['dinghy'] = True

    if not config['power_shell']:
        config['user_id'] = int(run('id -u', hide=True).stdout)

    if config['user_id'] > 256000:
        config['user_id'] = 1000

    return config


locals().update(__extract_runtime_configuration(locals()))
