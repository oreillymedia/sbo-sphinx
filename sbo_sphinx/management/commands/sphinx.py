import os

from shutil import copyfile, rmtree
from subprocess import Popen

from django.conf import settings
from django.core.management.base import BaseCommand

SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '..', '..'))

if hasattr(settings, 'SPHINX_INPUT_DIR'):
    INPUT_DIR = settings.SPHINX_INPUT_DIR
else:
    INPUT_DIR = 'doc'
INPUT_DIR = os.path.join(settings.ROOT_PATH, INPUT_DIR)

if hasattr(settings, 'SPHINX_OUTPUT_DIR'):
    OUTPUT_DIR = settings.SPHINX_OUTPUT_DIR
else:
    OUTPUT_DIR = '_build'
OUTPUT_DIR = os.path.join(settings.ROOT_PATH, OUTPUT_DIR)


class Command(BaseCommand):
    """
    Django management command for generating Sphinx documentation.
    """

    args = '<target>'
    help = 'Generate the documentation for this project using Sphinx'
    requires_model_validation = False
    temp_dirs = []
    temp_files = []

    def generate_python_docs(self):
        """
        Run sphinx-apidoc to generate Python API documentation for the project.
        """
        path = os.path.join(INPUT_DIR, 'python')
        if os.path.exists(path):
            rmtree(path)
        command = ['sphinx-apidoc', '-f', '-o', path,
                   '-H', settings.SPHINX_PROJECT_NAME, '..']
        # Exclude the temporary conf.py file
        command.append(os.path.join(INPUT_DIR, 'conf.py'))
        # Exclude anything else we were specifically asked to
        if hasattr(settings, 'SPHINX_PYTHON_EXCLUDE'):
            for exclude in settings.SPHINX_PYTHON_EXCLUDE:
                command.append(os.path.join(settings.ROOT_PATH, exclude))
        process = Popen(command, cwd=INPUT_DIR)
        process.wait()

    def copy_file(self, path, destination=None):
        """ Copy the file at the specified path (relative to the sbo_sphinx
        package directory) into the given directory relative to the Sphinx
        input directory, backing up any file that may already be there. """
        src = os.path.join(SOURCE_PATH, path)
        dst = INPUT_DIR
        if destination:
            parts = destination.split(os.path.sep)
            for part in parts:
                dst = os.path.join(dst, part)
                if not os.path.exists(dst):
                    os.mkdir(dst)
                    self.temp_dirs.append(dst)
        dst = os.path.join(dst, os.path.basename(path))
        if os.path.exists(dst):
            copyfile(dst, '%s.before_sphinx' % dst)
        copyfile(src, dst)
        self.temp_files.append(dst)

    def remove_temp_files(self):
        """ Remove any temporary files that were copied into the project's
        Sphinx input directory, restoring any files that may have been
        displaced by them. """
        for path in self.temp_files:
            dst = os.path.join(INPUT_DIR, path)
            os.remove(dst)
            src = '%s.before_sphinx' % dst
            if os.path.exists(src):
                copyfile(src, dst)
                os.remove(src)
        # This may have been generated during the run, get rid of it too
        path = os.path.join(INPUT_DIR, 'conf.pyc')
        if os.path.exists(path):
            os.remove(path)
        # Clean up the generated API reST files so we don't check them in
        path = os.path.join(INPUT_DIR, 'python')
        if os.path.exists(path):
            rmtree(path)
        self.temp_dirs.reverse()
        for directory in self.temp_dirs:
            os.rmdir(directory)

    def handle(self, *args, **options):
        """
        Temporarily copy the files needed to generate Sphinx documentation
        into the project root directory, generate the documentation, and then
        clean up the temporary files.
        """
        self.copy_file('Makefile')
        if len(args) < 1:
            process = Popen(['make'], cwd=INPUT_DIR)
            process.wait()
        else:
            env = os.environ.copy()
            # Get rid of any old generated output
            if os.path.exists(OUTPUT_DIR):
                rmtree(OUTPUT_DIR)
            os.makedirs(OUTPUT_DIR)
            env['BUILDDIR'] = OUTPUT_DIR
            self.copy_file('conf.py')
            self.copy_file(os.path.join('_static', 'favicon.ico'), '_static')
            self.copy_file(os.path.join('_static', 'safari_logo.png'),
                           '_static')
            if hasattr(settings, 'SPHINX_EXTERNAL_FILES'):
                for path in settings.SPHINX_EXTERNAL_FILES:
                    self.copy_file(os.path.join('..', path))
            self.generate_python_docs()
            process = Popen(['make', args[0]], cwd=INPUT_DIR, env=env)
            process.wait()
        self.remove_temp_files()
