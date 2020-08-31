from __future__ import print_function

from setuptools import find_packages
from setuptools import setup


version = "0.0.1"

setup_requires = []
install_requires = []

setup(
    name="depth_viewer",
    version=version,
    description="depth viewer",
    author="kosuke55",
    author_email="kosuke.tnp@gmail.com",
    url="https://github.com/kosuke55/depth_viewer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts':
        ['depth_viewer=depth_viewer.apps.view:main']},
    setup_requires=setup_requires,
    install_requires=install_requires,
)
