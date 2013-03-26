from fabric.api import lcd, local


def release(package):
    """ release [package] on pypi and update versions.cfg """
    with lcd('src/%s' % package):
        local('../../bin/prerelease')
        local('../../bin/release')
        version = local('../../bin/python setup.py --version', capture=True).strip()
        local('../../bin/postrelease')
    local(u"sed -i 's/\(%s = \)\(.*\)$/%s%s/g' versions/production.cfg" % (package, r'\1', version))
