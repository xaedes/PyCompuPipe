from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="pycompupipe",
    version="0.0.1",
    description="Python Computational Pipeline",
    long_description=readme(),
    url="https://github.com/xaedes/PyCompuPipe",
    author="xaedes",
    author_email="xaedes@gmail.com",
    license="MIT",
    packages=["pycompupipe","pycompupipe.components"],
    dependency_links=[
        "https://github.com/xaedes/testing/tarball/master",
        "https://github.com/xaedes/pyecs/tarball/master"
        ],
    tests_require=["pytest","pytest-mock","testing"],
    install_requires=[
        "funcy","pytest-runner","pyecs"
    ],
    include_package_data=True,
    zip_safe=False
    )
