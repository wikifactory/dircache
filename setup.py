from setuptools import find_packages, setup

VERSION = ""
tests_require = []

setup(
    name="diskcache",
    version=VERSION,
    description="File system directory cache",
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="filesystem cache lru dir directory folder",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "watchdog==0.8.3",
    ],
    tests_require=tests_require,
    extras_require={"test": tests_require},
    include_package_data=True,
    zip_safe=False,
    platforms="any",
)
