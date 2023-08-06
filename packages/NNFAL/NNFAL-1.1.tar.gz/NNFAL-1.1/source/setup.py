from setuptools import setup

setup(
    name='NNFAL-pre',
    version='1.0',
    packages=['NNFAL'],
    # install_requires=[
    #     'numpy',
    #     'torch',
    # ],
    entry_points={
        'console_scripts': [
            'installer = NNFAL-pre.installer:main'
        ]
    }
)
