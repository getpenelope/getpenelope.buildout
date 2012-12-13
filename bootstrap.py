##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id$
"""

import os, shutil, sys, tempfile, urllib2
from optparse import OptionParser

tmpeggs = tempfile.mkdtemp()
is_jython = sys.platform.startswith('java')

# parsing arguments
parser = OptionParser()
parser.add_option("-v", "--version", dest="version",
                          help="use a specific zc.buildout version")
parser.add_option("-d", "--distribute",
                   action="store_true", dest="distribute", default=False,
                   help="Use Distribute rather than Setuptools.")

parser.add_option("-c", None, action="store", dest="config_file",
                   help=("Specify the path to the buildout configuration "
                         "file to be used."))

options, args = parser.parse_args()

# if -c was provided, we push it back into args for buildout' main function
if options.config_file is not None:
    args += ['-c', options.config_file]

if options.version is not None:
    VERSION = '==%s' % options.version
else:
    VERSION = ''

USE_DISTRIBUTE = options.distribute
args = args + ['bootstrap']

to_reload = False
try:
    import pkg_resources
#    if not hasattr(pkg_resources, '_distribute'):
#        to_reload = True
#        raise ImportError
except ImportError:
    ez = {}
    if USE_DISTRIBUTE:
        exec urllib2.urlopen('http://python-distribute.org/distribute_setup.py'
                         ).read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0, no_fake=True)
    else:
        exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py'
                             ).read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)

    if to_reload:
        reload(pkg_resources)
    else:
        import pkg_resources

def quote (c):
    return c

cmd = 'from setuptools.command.easy_install import main; main()'
ws  = pkg_resources.working_set

if USE_DISTRIBUTE:
    requirement = 'distribute'
else:
    requirement = 'setuptools'

if is_jython:
    import subprocess

    assert subprocess.Popen([sys.executable] + ['-c', quote(cmd), '-mqNxd',
           quote(tmpeggs), 'zc.buildout' + VERSION],
           env=dict(os.environ,
               PYTHONPATH=
               ws.find(pkg_resources.Requirement.parse(requirement)).location
               ),
           ).wait() == 0

else:
    assert os.spawnle(
        os.P_WAIT, sys.executable, quote (sys.executable),
        '-c', quote (cmd), '-mqNxd', quote (tmpeggs), 'zc.buildout' + VERSION,
        dict(os.environ,
            PYTHONPATH=
            ws.find(pkg_resources.Requirement.parse(requirement)).location
            ),
        ) == 0

ws.add_entry(tmpeggs)
ws.require('zc.buildout' + VERSION)
import zc.buildout.buildout

def bootstrap(self, args):

    self._setup_directories()

    # Now copy buildout and setuptools eggs, and record destination eggs:
    entries = []
    for name in 'setuptools', 'zc.buildout':
        r = pkg_resources.Requirement.parse(name)
        dist = pkg_resources.working_set.find(r)
        if dist.precedence == pkg_resources.DEVELOP_DIST:
            dest = os.path.join(self['buildout']['develop-eggs-directory'],
                                name+'.egg-link')
            open(dest, 'w').write(dist.location)
            entries.append(dist.location)
        else:
            dest = os.path.join(self['buildout']['eggs-directory'],
                                os.path.basename(dist.location))
            entries.append(dest)
            if not os.path.exists(dest):
                if os.path.isdir(dist.location):
                    shutil.copytree(dist.location, dest)
                else:
                    shutil.copy2(dist.location, dest)

    # Create buildout script
    ws = pkg_resources.WorkingSet(entries)
    ws.require('zc.buildout')
    zc.buildout.easy_install.scripts(
        ['zc.buildout'], ws, sys.executable,
            self['buildout']['bin-directory'])

### monkey_patch
zc.buildout.easy_install.script_template = zc.buildout.easy_install.script_header + '''\
%(relative_paths_setup)s
import sys
sys.path[0:0] = [
    %(path)s,
    ]

%(initialization)s
import %(module_name)s

#################################
# RedTurtle URLopener patching  #
#################################

from urllib import splithost
import urllib, zc.buildout, urllib2, os
import getpass
try:
    import keyring
    import ConfigParser
    KEYRING = True
except ImportError:
    KEYRING = False

class PasswordOpener(urllib2.BaseHandler):

    def __init__(self, *args, **kwargs):
        self.type = 'http'
        self.auth_cache = {}
        self.tries = 0
        self.maxtries = 3
        self.tries_401 = {'dummy':0}

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 401 -- authentication required.
        See this URL for a description of the basic authentication scheme:
        http://www.ics.uci.edu/pub/ietf/http/draft-ietf-http-v10-spec-00.txt"""
        self.tries_401[url] = self.tries_401.get(url, -1) + 1

        if not 'www-authenticate' in headers:
            self.parent.http_error_default(self, url, fp,
                                         errcode, errmsg, headers)
        stuff = headers['www-authenticate']
        import re
        match = re.match('[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', stuff)
        if not match:
            self.parent.http_error_default(self, url, fp,
                                         errcode, errmsg, headers)
        scheme, realm = match.groups()
        if scheme.lower() != 'basic':
            self.parent.http_error_default(self, url, fp,
                                         errcode, errmsg, headers)
        name = 'retry_' + self.type + '_basic_auth'
        if not isinstance(url, basestring):
            url = url._Request__r_type
        if data is None:
            return getattr(self,name)(url, realm)
        else:
            return getattr(self,name)(url, realm, data)

    def retry_http_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        i = host.find('@') + 1
        host = host[i:]
        user, passwd = self.get_user_passwd(host, realm, i)
        if not (user or passwd): return None
        auth = "Basic " + urllib2.unquote(user +':'+ passwd).encode('base64').strip()
        newurl = 'http://' + host + selector
        request = urllib2.Request(newurl)
        request.add_header('Authorization', auth)
        if data is None:
            return self.parent.open(request)
        else:
            return self.parent.open(request, data)

    def retry_https_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        i = host.find('@') + 1
        host = host[i:]
        user, passwd = self.get_user_passwd(host, realm, i)
        if not (user or passwd): return None
        auth = "Basic " + urllib2.unquote(user + ':' + passwd).encode('base64').strip()
        newurl = 'https://' + host + selector
        request = urllib2.Request(newurl)
        request.add_header('Authorization', auth)
        return self.parent.open(request, data)

    def get_user_passwd(self, host, realm, clear_cache = 0):
        key = realm + '@' + host.lower()
        if key in self.auth_cache:
            if clear_cache:
                del self.auth_cache[key]
            else:
                return self.auth_cache[key]
        user, passwd = self.prompt_user_passwd(host, realm)
        if user or passwd: self.auth_cache[key] = (user, passwd)
        return user, passwd

    def prompt_user_passwd(self, host, realm):
        """Override this in a GUI environment!"""
        if KEYRING:
            return keyring_prompt(realm, host, max(self.tries_401.values()))
        else:
            try:
                user = raw_input("Enter username for " + realm + " at " + host + ": ")
                passwd = getpass.getpass("Enter password for " + user + " in " + realm + " at " + host  + ": ")
                return user, passwd
            except KeyboardInterrupt:
                print
                return None, None

def keyring_prompt(realm, host, tries):
    #First try to take it from keyring
    # config file init
    try:
        config_file = os.path.join(os.path.expanduser('~'),
              '.buildout',
              'keyring.cfg')
        file(config_file)
    except IOError, e:
        open(config_file, 'w').close() 

    config = ConfigParser.SafeConfigParser({ 'username':'', })
    config.read(config_file)
    if not config.has_section(realm):
        config.add_section(realm)
    username = config.get(realm,'username')
    password = None
    if username != '':
        if tries:
            keyring.set_password(realm, username, '')
        else:
            password = keyring.get_password(realm, username)
    if not password:
        username = raw_input("Enter username for " + realm + " at " + host + ": ")
        password = getpass.getpass("Enter password for " + username + " in " + realm + " at " + host  + ": ")

        config.set(realm, 'username', username)
        config.write(open(config_file, 'w'))

        # store the password
        keyring.set_password(realm, username, password)
    return username, password


class CredHandler(urllib.FancyURLopener):

    tries_401 = {'dummy':0}

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 401 -- authentication required.
        See this URL for a description of the basic authentication scheme:
        http://www.ics.uci.edu/pub/ietf/http/draft-ietf-http-v10-spec-00.txt"""
        self.tries_401[url] = self.tries_401.get(url, -1) + 1
        return urllib.FancyURLopener.http_error_401(self,url,fp,errcode,errmsg,headers,data=None)

    def prompt_user_passwd(self, host, realm):
        if KEYRING:
            return keyring_prompt(realm, host, max(self.tries_401.values()))
        else:
            return urllib.FancyURLopener.prompt_user_passwd(self, host, realm)


zc.buildout.download.url_opener = CredHandler()
urllib2.install_opener(urllib2.build_opener(PasswordOpener))


if __name__ == '__main__':
    %(module_name)s.%(attrs)s(%(arguments)s)
'''


zc.buildout.buildout.Buildout.bootstrap = bootstrap
zc.buildout.buildout.main(args)
shutil.rmtree(tmpeggs)

