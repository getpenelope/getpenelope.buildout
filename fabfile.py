from fabric.api import lcd, local, run, cd, env, quiet, sudo, get
from fabric.utils import abort
from fabric.colors import green, red
from fabric.network import needs_host, normalize
from subprocess import Popen

def release(package):
    """ release [package] on pypi and update versions.cfg """
    with lcd('src/%s' % package):
        local('../../bin/prerelease')
        local('../../bin/release')
        version = local('../../bin/python setup.py --version', capture=True).strip()
        local('../../bin/postrelease')
    local(u"sed -i 's/\(%s = \)\(.*\)$/%s%s/g' versions/production.cfg" % (package, r'\1', version))
    local("git add versions/production.cfg")
    local("git commit -m 'update production versions for %s'" % package)
    local("git push")

def production():
    """Use production server"""
    if not 'penelope.production.server' in env \
            or not 'penelope.production.dir' in env \
            or not 'penelope.production.user' in env:
        abort('You don\'t have proper production ENV. '
              'Please check your ~/.fabricrc '
              'and ensure that you have two entries:\n' + \
              green('penelope.production.server = example.com\n') + \
              green('penelope.production.user = user\n') + \
              green('penelope.production.dir = /opt/my_dir'))

    env.directory = env['penelope.production.dir']
    env.hosts = [env['penelope.production.server']]
    env.user = env['penelope.production.user']

def dev():
    """Use local development server"""
    with quiet():
        env.directory = local('pwd', capture=True)

def staging():
    """Use staging server"""
    if not 'penelope.staging.server' in env \
            or not 'penelope.staging.dir' in env \
            or not 'penelope.staging.user' in env:
        abort('You don\'t have proper staging ENV. '
              'Please check your ~/.fabricrc '
              'and ensure that you have two entries:\n' + \
              green('penelope.staging.server = example.com\n') + \
              green('penelope.staging.user = user\n') + \
              green('penelope.staging.dir = /opt/my_dir'))

    env.directory = env['penelope.staging.dir']
    env.hosts = [env['penelope.staging.server']]
    env.user = env['penelope.staging.user']

def _co(package, branch, _cd, _run, **kwargs):
    """git checkout [branch] of a specific [package]"""
    packages_dir = '%s/src' % env.directory
    with _cd(packages_dir):
        if not _run('ls -d * | grep %s | cat' % package, **kwargs):
            print red('package [%s] not found' % package)
            return
    with _cd('%s/%s' % (packages_dir, package)):
        _run("git pull")
        if not _run('git branch -r | grep %s | cat' % branch, **kwargs):
            print red('[%s] not found for package [%s]' % (branch, package))
            return
        print green('checkout [%s] for package [%s]' % (branch, package))
        _run("git checkout master")
        _run("git pull")
        _run('git checkout %s' % branch)

def co(package, branch='master'):
    """git checkout [branch] of a specific [package]"""
    if not 'directory' in env:
        abort('Usage: $ fab [production|staging|dev] co:package_name')
    with quiet():
        if env.hosts:
            _co(package, branch, cd, run, quiet=True)
        else:
            _co(package, branch, lcd, local, capture=True)

def _pullower(branch, _cd, _run, **kwargs):
    packages_dir = '%s/src' % env.directory
    with _cd(packages_dir):
        output = _run('ls -d *', **kwargs)
        packages = output.split()
    for package in packages:
        _co(package, branch, _cd, _run, **kwargs)

def pullower(branch='master'):
    """ tries to pull [branch] from all sources """
    if not 'directory' in env:
        abort('Usage: $ fab [production|staging|dev] pullrequest:branch')
    with quiet():
        if env.hosts:
            _pullower(branch, cd, run, quiet=True)
        else:
            _pullower(branch, lcd, local, capture=True)

def buildout():
    """Pull buildout, run bin/buildount, touch wsgi"""
    with cd(env.directory):
        run("git pull")
        run("./bin/buildout -NU")
        run("./bin/solr-instance stop")
        run("./bin/solr-instance start")
        run("touch parts/mod_wsgi/wsgi")

def sync_postgres(hostname):
    with cd('/tmp'):
        sudo('pg_dump por > /tmp/por.dump', user='postgres')
    get('/tmp/por.dump', local_path='/tmp')
    proc = Popen(['sudo','-u', 'postgres', 'dropdb', 'por'])
    if proc.wait():
        return
    proc = Popen(['sudo','-u', 'postgres', 'createdb', 'por'])
    if proc.wait():
        return
    proc = Popen(['sudo','-u', 'postgres', 'psql', '-d', 'por', '-f', '/tmp/por.dump'])
    if proc.wait():
        return
    proc = Popen(['sudo','-u', 'postgres', 'psql', '-d', 'por', '-c', 'update applications set api_uri = replace(api_uri, \'https://penelope.redturtle.it\', \'%s\');' % hostname])
    if proc.wait():
        return

@needs_host
def sync_var():
    """Sync buildout var folder"""
    user, host, port = normalize(env.host_string)
    with quiet():
        local_buildout = local('pwd', capture=True)
    cmd = 'rsync --exclude \'data\' --exclude \'.log\' --exclude \'svnenvs\' --exclude \'cache\' -pthrvz %s@%s:%s%s %s%s' % (user, host,
                                                                                                                            env.directory, '/var/',
                                                                                                                            local_buildout, '/var/')
    local(cmd)
