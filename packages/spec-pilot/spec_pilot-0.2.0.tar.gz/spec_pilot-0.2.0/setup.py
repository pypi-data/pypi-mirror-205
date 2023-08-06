import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.execute(lambda: self.download_spacy_model(), [])

    @staticmethod
    def download_spacy_model():
        os.system("python -m spacy download en_core_web_sm")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spec_pilot",
    version="0.2.0",
    author="jmfwolf",
    author_email="jmfwolf@hacksomniac.com",
    description="A tool to generate OpenAPI specifications using natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmfwolf/spec-pilot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.6',
    install_requires=[
        "spacy>=3.5.2",
        "PyYAML>=6.0",
        "pystache>=0.6.0",
],
    entry_points={
        'console_scripts': [
            'spec-pilot=spec_pilot:main',
        ],
    },
    cmdclass={"install": PostInstallCommand},
)
