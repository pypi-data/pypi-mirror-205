import os
from setuptools import setup, find_packages
from bam_core.__version__ import VERSION

reqs = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "requirements.txt")
)
with open(reqs) as f:
    install_requires = [req.strip().split("==")[0] for req in f]

config = {
    "name": "bam-core",
    "version": VERSION,
    "packages": find_packages(),
    "install_requires": install_requires,
    "author": "BAM",
    "author_email": "hola@bushwickayudamutua.com",
    "description": "Shared code for BAM Automations",
    "url": "http://bushwickayudamutua.org",
}

setup(**config)
