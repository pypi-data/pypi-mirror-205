from setuptools import setup

setup(
    name='NNFAL',
    version='1.8',
    packages=['source'],
    package_data={'NNFAL': ['xspeed.py']},
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
