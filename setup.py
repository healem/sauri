from distutils.core import setup

setup(
    name='Sauri',
    author='Mike Healey',
    author_email='healem@alum.rpi.edu',
    url='https://github.com/healem/sauron',
    version='0.1',
    packages=['sauri.common',
              'sauri.messaging',
              'sauri.sensors',],
    license='MIT',
    long_description=open('README').read(),
)