from setuptools import setup
from os import path
here = path.abspath(path.dirname(__file__))

setup(
    name='biQPS',
    version='0.0.1',
    description = ("An Open Software for Bitstream-based Quality Prediction in Adaptive Streaming"),
    packages=['biQPS'],
    package_data={
        '': ['biQPS/LSTM/*']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'biQPS = biQPS.__main__:main'
        ]
    },
)