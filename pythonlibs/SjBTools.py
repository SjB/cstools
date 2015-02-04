# -*- coding: UTF-8 -*-
#
# Tools/pythonlibs/SjBTools.py
# Copyright © 2015 SjB <steve@sagacity.ca>. All Rights Reserved.

import sys
import os
import subprocess
import urllib
import shutil

protobuild_url = 'https://github.com/hach-que/Protobuild/blob/master/Protobuild.exe?raw=true'

def getplatform():
    p = sys.platform
    if p.startswith('linux'):
        return 'Linux'
    elif p == 'darwin':
        return 'MacOS'
    elif p == 'win32':
        return 'Windows'

    print("Unsuppored Platform.")
    return ''


def run(*args, **kwargs):
    returncode = subprocess.call(*args, **kwargs)
    if returncode != 0:
        sys.exit(returncode)

def nuget(thirdparty_libdir, package, version=None):
    cmd = ['nuget.exe', 'install', '-OutputDirectory', thirdparty_libdir]
    cmd.append(package)
    if version:
        cmd.extend(['-version', version])

    run(cmd)

def build(solution, args):
    platform = getplatform()
    build_tool = 'xbuild'
    if "Windows" == platform:
        build_tool='msbuild'

    cmd = [build_tool, solution]
    cmd.extend(args)

    run(cmd)

def wget(url, filename=None):
    if filename:
        dir = os.path.dirname(filename)
        if dir and not os.path.exists(dir):
            os.makedirs(dir)

    (filename, header) = urllib.urlretrieve(url, filename)
    print('Fetching: ' + filename)

def gitclone(repo, path):
    if not os.path.exists(path):
        run(['/usr/bin/git', 'clone', repo, path])  

class Protobuild:

    def __init__(self, workspace):
        self.workspace = workspace
        self.cliapp = os.path.join(workspace, 'Protobuild.exe')

    def generate(self, platform = None):
        if platform == None:
            platform = getplatform()
        self.run('-generate', platform)

    def run(self, *args):
        cmd = []

        platform = getplatform()
        if "Windows" != platform:
            cmd.append('/usr/bin/mono')

        cmd.append(self.cliapp)
        cmd.extend(args)

        if os.path.exists(self.cliapp):
            run(cmd)
            return True

        print("Missing %s." % self.cliapp)
        return False

    def exists(self):
        return os.path.exists(self.cliapp)

    def fetch(self):
        wget(protobuild_url, filename=self.cliapp)

    def clean(self, platform = None, exclude = []):
        if platform == None:
            platform = getplatform()

        self.run('-clean', platform)

        exclude.append('.git')
        for root, dirs, files in os.walk(self.workspace):
            for name in dirs:
                if name in exclude:
                    continue

                if name in ['obj', 'bin']:
                    p = os.path.join(root, name)
                    print("Removing: %s" % p)
                    shutil.rmtree(p);


