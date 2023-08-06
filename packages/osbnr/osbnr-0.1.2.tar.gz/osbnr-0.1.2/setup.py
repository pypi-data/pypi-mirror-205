from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='osbnr',
    version='0.1.2',
    description='One Side Behavioral Noise Reduction algorithm implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Salma EL HAJJAMI',
    author_email='s.elhajjami@uiz.ac.ma',
    packages=find_packages(),
    install_requires=['scikit-learn', 'numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
