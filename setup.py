from setuptools import setup

setup(
   name='supervisor_compressor',
   version='1.1',
   description='Sistema supervisório para compressor',
   author='Beatriz, Sabrina e Marcos',
   packages=['supervisor_compressor'],  #same as name
   install_requires=['kivy', 'kivy_garden', 'pymodbustcp', 'pymodbus', 'sqlalchemy'], #external packages as dependencies
)