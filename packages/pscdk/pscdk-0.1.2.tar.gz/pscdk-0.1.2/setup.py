
import os
import shutil
import setuptools
# from skbuild import setup
from distutils.core import setup

from distutils.sysconfig import get_python_lib
import glob

release_files = []
for d in ["pysrc/codon"]:
    for root, dirs, files in os.walk(d):
        for f in files:
            release_files.append(os.path.join(root.replace('pysrc/', ''), f))

for root, dirs, files in os.walk("pysrc/templates"):
    for f in files:
        release_files.append(os.path.join(root.replace('pysrc/', ''), f))    

setup(
    name="pscdk",
    version="0.1.2",
    description="Python Smart Contract Development Kit",
    author='The UUOSIO Team',
    license="Commercial",
    url="https://github.com/uuosio/pscdk",
    packages=['pscdk'],
    package_dir={'pscdk': 'pysrc'},
    package_data={
#        "": ["*"],
        'pscdk': release_files,
    },
    setup_requires=['wheel']
    # scripts=['compiler/build/release/tinygo/bin/eosio-go'],
    # install_requires=[
    # ],
    # include_package_data=True
)
