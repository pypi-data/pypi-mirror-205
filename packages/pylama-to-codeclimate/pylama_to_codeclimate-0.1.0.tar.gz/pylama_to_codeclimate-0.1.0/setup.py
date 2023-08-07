from setuptools import setup
from os import path

with open(path.join(path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='pylama_to_codeclimate',
    version='0.1.0',
    description='Convert pylama output to codeclimate format',
    long_description=long_description,
    url='https://github.com/sapher/pylama_to_codeclimate',
    author='Anonymous',
    author_email='anonymous@anonymous.anon',
    license='WTFPL',
    py_modules=['pylama_to_codeclimate'],
    setup_requires=['setuptools_scm'],
    entry_points={
        'console_scripts': [
            'pylama_to_codeclimate=pylama_to_codeclimate:main',
        ],
    },
)
