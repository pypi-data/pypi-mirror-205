from setuptools import find_packages, setup

setup(
    name="BlockFrame",
    version="0.1.4",
    author="Rohaan Ahmed",
    author_email="silent.death3500@gmail.com",
    description="File Chunking Library to work as a data-store solution alongside webapps and software.",
    packages=find_packages(),
    install_requires=["cryptography", "SQLAlchemy", "setuptools", "wheel", "aiosqlite"],
    url="https://github.com/Wizock/BlockFrame/",
)
