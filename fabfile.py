from fabric.api import lcd, local, run, cd, env
from fabric.utils import abort
from fabric.colors import green


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

def staging():
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

def co(package, branch='master'):
    """git checkout [branch] of a specific [package]"""
    with cd('%s/src/%s' % (env.directory, package)):
        run("git checkout master", quiet=True)
        run("git pull", quiet=True)
        run('git checkout %s' % branch)

def buildout():
    with cd(env.directory):
        run("git pull")
        run("./bin/buildout -NU")
        run("touch parts/mod_wsgi/wsgi")
