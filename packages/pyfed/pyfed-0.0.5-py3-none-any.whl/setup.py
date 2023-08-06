import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name="PyFed",
    version="0.0.4",
    author = "Amirreza Sokhankhosh",
    author_email = "amirreza.sokhankhosh@gmail.com",
    description = "PyFed is an open-source framework for federated learning algorithms.",
    long_description=read('./README.md'),
    install_requires=['h5py', 'numpy', 'tensorflow'],
    license = "MIT",
    url="https://github.com/amirrezasokhankhosh/PyFed",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )