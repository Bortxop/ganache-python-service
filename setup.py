from setuptools import setup, find_packages

setup(
    name='ganache_python_serv',
    version='0.3.1',
    packages=find_packages(exclude=["test", "tests.*"]),
    install_requires=['psutil'
                     ],
    author='Borja León',
    author_email='borja.l.murua@gmail.com',
    description='Library to interact directly with ganache',
    license='MIT',
    keywords='ganache, python, ethereum, blockchain, testing',
    url='https://github.com/Bortxop/ganache-python-service'
)