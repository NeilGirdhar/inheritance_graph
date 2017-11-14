from setuptools import find_packages, setup

setup(
    name='inheritance_graph',
    packages=find_packages(),
    version='0.3',
    description='A tool to help debug inheritance failures.',
    author='Neil Girdhar',
    author_email='mistersheik@gmail.com',
    url='https://github.com/NeilGirdhar/inheritance_graph',
    download_url='https://github.com/neilgirdhar/inheritance_graph/archive/0.3.tar.gz',
    keywords=['inheritance', 'debugging'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires = ['networkx>=2.0',
                        'more-itertools>=3.2.0'],
    python_requires='>=3.4'
)
