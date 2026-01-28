from setuptools import setup, find_packages

requirements = [ 'pyyaml' ]

setup(
    author="nbtm-sh",
    author_email="n.glades@unsw.edu.au",
    description="yaml configuration file wrapper",
    install_requires=requirements,
    packages=find_packages(include=['kagemori_config_manager']),
    version="0.1rc1",
    name="kagemori-config-manager"
)
