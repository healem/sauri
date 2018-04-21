from setuptools import setup

setup(
    name='Sauri',
    author='Mike Healey',
    author_email='healem@alum.rpi.edu',
    description='Simple home automation script in the early phases of development'
    url='https://github.com/healem/sauri',
    version='0.4',
    packages=['sauri',
              'sauri.common',
              'sauri.messaging',
              'sauri.messaging.blocking',
              'sauri.messaging.blocking.test',
              'sauri.sensors',
              'sauri.sensors.test',
              'sauri.sensors.temperature',
              'sauri.sensors.temperature.test',],
    install_requires=['mock',
                      'coverage',
                      'PyYAML',
                      'pika',],
    include_package_data=True,
    license='MIT',
    long_description=open('README').read(),
)