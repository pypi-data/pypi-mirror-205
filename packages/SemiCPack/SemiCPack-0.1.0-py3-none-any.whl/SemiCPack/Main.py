from setuptools import setup, find_packages

setup(
    name='SemiCPack',
    version='0.1.0',
    description='A Python plugin for GUI support',
    packages=find_packages(),
    install_requires=[
        # list the packages that your plugin depends on here
    ],
    entry_points={
        'console_scripts': [
            'SemiCPack=SemiCPack.main:main',
        ],
    },
)
