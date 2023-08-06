from setuptools import setup, find_packages

setup(
    name='Foodfacts',
    version='0.1',
    description='A library that displays one food fact every 24 hours',
    author='Naseem',
    author_email='ns.sultana93@gmail.com',
    packages=find_packages(),
    install_requires=[
        'datetime',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)