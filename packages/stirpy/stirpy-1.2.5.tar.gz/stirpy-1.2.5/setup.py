import setuptools

setuptools.setup(
    name='stirpy',
    version='1.2.5',
    description='A Powerful scientific strings-processing library called stirpy',
    install_requires=['numpy', 'nltk', 'afinn', 'wheel', 'tqdm', 'setuptools'],
    author='KhalidAghrini',
    author_email='kwaaghrini@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
