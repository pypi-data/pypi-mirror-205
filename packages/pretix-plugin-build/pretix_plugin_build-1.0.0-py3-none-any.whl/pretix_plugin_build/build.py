import os

from django.core import management
from setuptools.command.build import build

here = os.path.abspath(os.path.dirname(__file__))
npm_installed = False


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)
