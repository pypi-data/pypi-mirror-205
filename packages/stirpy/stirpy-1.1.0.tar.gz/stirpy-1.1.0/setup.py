from setuptools import setup, find_packages

with open("stripy.py", "r") as fh:
    long_description = fh.read()

setup(
    name='stirpy',
    version='1.1.0',
    author='KhalidWalidAghrini',
    author_email='kwaaghrini@gmail.com',
    description='A Powerful scientific strings-processing library called stipy',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'nltk',
        'afinn',
        're',
        'os'
    ],
)