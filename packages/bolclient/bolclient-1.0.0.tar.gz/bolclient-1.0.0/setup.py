from setuptools import setup

setup(
    name='bolclient',
    version='1.0.0',
    description='Bol.com api client running on version v8',
    url='https://gitlab.com/bolooco/bol-client',
    author='Boloo',
    license='MIT',
    packages=['bolclient'],
    install_requires=[
        'requests',
        'redis',
    ],
    zip_safe=False
)
