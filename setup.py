from setuptools import setup, find_packages

version = '1.0'

setup(
    name="sbo-sphinx",
    version=version,
    author="Jeremy Bowman",
    author_email="jbowman@safaribooksonline.com",
    description="Sphinx configuration and libraries for SBO documentation",
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        'Django>=1.4.3',
        'django-nose',
        'Sphinx',
        'javasphinx',
    ],
)
