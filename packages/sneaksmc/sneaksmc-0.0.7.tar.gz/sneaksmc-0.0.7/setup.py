from setuptools import setup, find_packages


setup(
    name='sneaksmc',
    version='0.0.7',
    license='MIT',
    author="tsy",
    author_email='torkus88@hotmail.com',
    packages=find_packages(),
    package_dir={'src': 'sneaksmc'},
    url='http://www.example.com',
    keywords='smc, secure, server, cryptography, crypt, Secure multiparty computation',
    install_requires=['pycrypto', 'rsa'],

)
