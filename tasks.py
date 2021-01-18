from invoke import task
from shlex import quote
from colorama import Fore


def build(c):
    """
    Build the infrastructure
    """
    command = 'build'
    command += ' --build-arg PROJECT_NAME=%s' % c.project_name
    command += ' --build-arg USER_ID=%s' % c.user_id

    with Builder(c):
        docker_compose(c, command)


@task
def up(c):
    """
    Ensure infrastructure is sync and running
    """
    build(c)
    docker_compose(c, 'up --remove-orphans -d')


@task
def start(c):
    """
    Be sure that everything is started and installed
    """
    if c.dinghy:
        machine_running = c.local('dinghy status').stdout
        if machine_running.splitlines()[0].strip() != 'VM: running':
            c.local('dinghy up --no-proxy')
            c.local('docker-machine ssh dinghy "echo \'nameserver 8.8.8.8\' | sudo tee -a /etc/resolv.conf && sudo /etc/init.d/docker restart"')

    up(c)
    cache_clear(c)
    install(c)

    print(Fore.GREEN + 'You can now browse:')
    for domain in [c.root_domain] + c.extra_domains:
        print(Fore.YELLOW + "* https://" + domain)


@task
def install(c):
    """
    Install frontend application (composer, yarn, assets)
    """
    with Builder(c):
        docker_compose_run(c, 'composer install -n --prefer-dist --optimize-autoloader', no_deps=True)


@task
def cache_clear(c):
    """
    Clear cache of the frontend application
    """
    with Builder(c):
        docker_compose_run(c, 'rm -rf var/cache/', no_deps=True)


@task
def builder(c):
    """
    Bash into a builder container
    """
    with Builder(c):
        docker_compose_run(c, 'bash')


@task
def logs(c):
    """
    Show logs of infrastructure
    """
    docker_compose(c, 'logs -f --tail=150')


@task
def stop(c):
    """
    Stop the infrastructure
    """
    docker_compose(c, 'stop')


@task
def down(c):
    """
    Clean the infrastructure (remove container, volume, networks)
    """
    with Builder(c):
        docker_compose(c, 'down --volumes --rmi=local')


def run_in_docker_or_locally_for_dinghy(c, command, no_deps=False):
    """
    Mac users have a lot of problems running Yarn / Webpack on the Docker stack so this func allow them to run these tools on their host
    """
    if c.dinghy:
        with c.cd(c.project_directory):
            c.run(command)
    else:
        docker_compose_run(c, command, no_deps=no_deps)


def docker_compose_run(c, command_name, service="builder", user="app", no_deps=False, workdir=None, port_mapping=False):
    args = [
        'run',
        '--rm',
        '-u %s' % quote(user),
    ]

    if no_deps:
        args.append('--no-deps')

    if port_mapping:
        args.append('--service-ports')

    if workdir is not None:
        args.append('-w %s' % quote(workdir))

    docker_compose(c, '%s %s /bin/sh -c "exec %s"' % (
        ' '.join(args),
        quote(service),
        command_name
    ))


def docker_compose(c, command_name):

    env = {
        'PROJECT_NAME': c.project_name,
        'PROJECT_DIRECTORY': c.project_directory,
        'PROJECT_ROOT_DOMAIN': c.root_domain,
    }

    cmd = 'docker-compose -p %s %s %s' % (
        c.project_name,
        ' '.join('-f \'' + c.root_dir + '/infrastructure/docker/' + file + '\'' for file in c.docker_compose_files),
        command_name
    )

    c.run(cmd, pty=True, env=env)

class Builder:
    def __init__(self, c):
        self.c = c

    def __enter__(self):
        self.docker_compose_files = self.c.docker_compose_files
        self.c.docker_compose_files = ['docker-compose.builder.yml'] + self.docker_compose_files

    def __exit__(self, type, value, traceback):
        self.c.docker_compose_files = self.docker_compose_files
