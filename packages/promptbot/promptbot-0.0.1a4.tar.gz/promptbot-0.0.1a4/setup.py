import os

from setuptools import setup

requirements = [
    "toml==0.10.2",
    "openai==0.27.5",
    "colorama==0.4.6",
]

curdir = os.path.dirname(__file__)

requirements = open(os.path.join(curdir, 'requirements.txt')).read()

readme = open(os.path.join(curdir, 'README.md')).read()

setup(
    name='promptbot',
    version='0.0.1-alpha.4',
    author='Clayton Bezuidenhout',
    author_email='claytonbez.nl@gmail.com',
    description='A Python package for generating prompt bots on top of OpenAI GTP Apis.',
    long_description=f"""{readme}""",
    long_description_content_type='text/markdown',
    packages=['promptbot'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
