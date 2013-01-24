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

    def generate_javascript_docs(self):
        """
        Use jsdoc-toolkit and jsdoc-toolkit-rst-template to generate JavaScript
        API documentation for the project.  Depends on having JSDoc formatted
        comments in the source code, without that this won't do much.  If the
        project contains no JavaScript or the JS files haven't been given JSDoc
        comments yet, just don't set SPHINX_JS_ROOT and this step will be
        skipped.
        """
        if not hasattr(settings, 'SPHINX_JS_ROOT'):
            return
        self.remove('javascript')
        jsdoc_toolkit_dir = os.path.join(SOURCE_PATH, 'jsdoc-toolkit')
        jsdoc_rst_dir = os.path.join(SOURCE_PATH, 'jsdoc-toolkit-rst-template')
        js_root = os.path.join(settings.ROOT_PATH, settings.SPHINX_JS_ROOT)
        build_xml_path = os.path.join(jsdoc_rst_dir, 'build.xml')
        command = ['ant', '-f', build_xml_path,
                   '-Djsdoc-toolkit.dir=%s' % jsdoc_toolkit_dir,
                   '-Djs.src.dir=%s' % js_root,
                   '-Djs.rst.dir=%s' % os.path.join(INPUT_DIR, 'javascript')]
        process = Popen(command, cwd=settings.ROOT_PATH)
        process.wait()
        # Convert the absolute paths in the file listing to relative ones
        if js_root[-1] != os.path.sep:
            js_root += os.path.sep
        path = os.path.join(INPUT_DIR, 'javascript', 'files.rst')
        with open(path, 'r') as f:
            content = f.read()
        content = content.replace(js_root, '')
        with open(path, 'w') as f:
            f.write(content)

    def generate_python_docs(self):
        """
        Run sphinx-apidoc to generate Python API documentation for the project.
        """
        self.remove('python')
        path = os.path.join(INPUT_DIR, 'python')
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
        self.remove('conf.pyc')
        # Clean up the generated API reST files so we don't check them in
        self.remove('javascriptAnd')
        self.remove('python')
        self.temp_dirs.reverse()
        for directory in self.temp_dirs:
            os.rmdir(directory)

    def remove(self, path):
        """
        Remove the directory or file at the specified path (relative to
        SPHINX_INPUT_DIR) if it exists.  Used when cleaning up after a build.
        """
        path = os.path.join(INPUT_DIR, path)
        if not os.path.exists(path):
            return
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)

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
                    self.copy_file(os.path.join(settings.ROOT_PATH, path))
            self.generate_python_docs()
            self.generate_javascript_docs()
            process = Popen(['make', args[0]], cwd=INPUT_DIR, env=env)
            process.wait()
        self.remove_temp_files()
