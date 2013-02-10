import pyasana

from distutils.core import setup


setup(
    name="pyasana",
    packages=["pyasana"],
    package_dir={"pyasana": "pyasana"},
    version=pyasana.__version__,
    description="Python Client for asana.com",
    long_description=open("README.rst").read() + "\n\n" + open("HISTORY.rst").read(),
    author="Casey Dunham",
    author_email="casey.dunham@gmail.com",
    url="https://github.com/caseydunham/python-asana",
    license=open("LICENSE").read(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ),
)
