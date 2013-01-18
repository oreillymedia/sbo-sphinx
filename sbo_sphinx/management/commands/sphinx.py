import os
import shutil

from subprocess import Popen

from django.conf import settings
from django.core.management.base import BaseCommand

SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '..', '..'))


class Command(BaseCommand):
    args = '<target>'
    help = 'Generate the documentation for this project using Sphinx'
    requires_model_validation = False

    def handle(self, *args, **options):
        makefile_path = os.path.join(settings.ROOT_PATH, 'Makefile')
        print makefile_path
        shutil.copyfile(os.path.join(SOURCE_PATH, 'Makefile'), makefile_path)
        if len(args) < 1:
            process = Popen(['make'], cwd=settings.ROOT_PATH)
            # Give it a second to finish printing the usage before exiting
            process.wait()
        else:
            env = os.environ.copy()
            if hasattr(settings, 'SPHINX_OUTPUT_DIR'):
                build_dir = settings.SPHINX_OUTPUT_DIR
            else:
                build_dir = '_build'
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
            env['BUILDDIR'] = build_dir
            conf_path = os.path.join(settings.ROOT_PATH, 'conf.py')
            shutil.copyfile(os.path.join(SOURCE_PATH, 'conf.py'), conf_path)
            process = Popen(['make', args[0]], cwd=settings.ROOT_PATH, env=env)
            process.wait()
            os.remove(conf_path)
        os.remove(makefile_path)
