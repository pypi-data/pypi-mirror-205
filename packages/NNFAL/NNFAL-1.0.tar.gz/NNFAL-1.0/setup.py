from setuptools import setup

setup(
    name='NNFAL',
    version='1.0',
    packages=['source'],
    # install_requires=[
    #     'numpy',
    #     'torch',
    # ],
    entry_points={
        'console_scripts': [
            'NNFAL = source.NNFAL:main'
        ]
    }
)
