from setuptools import setup

setup(
    name='NNFAL',
    version='1.10',
    packages=['source'],
    package_data={'source': ['source']},
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
