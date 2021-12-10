from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gado',
    version='0.0.2',
    license='MIT',
    author="Dikson Santos",
    author_email='diksonfer@gmail.com',
    description="generate poetry with gcc diagnostics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('gado'),
    package_dir={'': 'gado'},
    url='https://github.com/diksown/gado',
    keywords='gcc poetry nlp',
    install_requires=[
        'pronouncing',
        'requests',
        'pyxdg',
    ],
    entry_points={
        'console_scripts': [
            'gado = gado:main',
            'gado++ = gado:main',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Environment :: Console",
    ),
)
