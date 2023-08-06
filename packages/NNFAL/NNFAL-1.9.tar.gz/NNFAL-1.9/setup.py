from setuptools import setup

setup(
    name='NNFAL',
    version='1.9',
    packages=['source'],
    package_data={'NNFAL': ['source']},
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
