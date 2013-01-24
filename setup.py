from setuptools import setup, find_packages

version = '1.0'

setup(
    name="sbo-sphinx",
    version=version,
    author="Jeremy Bowman",
    author_email="jbowman@safaribooksonline.com",
    description="Sphinx configuration and libraries for SBO documentation",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        'sbo_sphinx': [
            'Makefile',
            '_static/favicon.ico',
            '_static/safari_logo.png',
            'jsdoc-toolkit/*.jar',
            'jsdoc-toolkit/*.sh',
            'jsdoc-toolkit/*.txt',
            'jsdoc-toolkit/app/*.js',
            'jsdoc-toolkit/app/frame/*.js',
            'jsdoc-toolkit/app/handlers/*.js',
            'jsdoc-toolkit/app/handlers/XMLDOC/*.js',
            'jsdoc-toolkit/app/lib/*.js',
            'jsdoc-toolkit/app/lib/JSDOC/*.js',
            'jsdoc-toolkit/app/plugins/*.js',
            'jsdoc-toolkit/app/t/*.js',
            'jsdoc-toolkit/app/test/*.js',
            'jsdoc-toolkit/app/test/scripts/*.js',
            'jsdoc-toolkit/app/test/scripts/*.txt',
            'jsdoc-toolkit/conf/*.conf',
            'jsdoc-toolkit/java/*.xml',
            'jsdoc-toolkit/java/classes/*.jar',
            'jsdoc-toolkit/java/src/*.java',
            'jsdoc-toolkit/templates/jsdoc/*.tmpl',
            'jsdoc-toolkit/templates/jsdoc/static/*.css',
            'jsdoc-toolkit/templates/jsdoc/static/*.html',
            'jsdoc-toolkit-rst-template/*.properties',
            'jsdoc-toolkit-rst-template/*.xml',
            'jsdoc-toolkit-rst-template/templates/rst/*.tmpl',
            'jsdoc-toolkit-rst-template/templates/rst/*.js',
        ],
    },
    zip_safe=False,
    dependency_links=[
        'https://bitbucket.org/jmbowman/sphinx/get/apidoc-exclude-files.tar.gz#egg=Sphinx-1.1.4',
    ],
    install_requires=[
        'Django>=1.4.3',
        'django-nose',
        'Sphinx>=1.1.4',
        'javasphinx',
    ],
)
