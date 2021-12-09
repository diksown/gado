from setuptools import setup, find_packages

setup(
    name='gado',
    version='0.0.1',
    license='MIT',
    author="Dikson Santos",
    author_email='diksonfer@gmail.com',
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
)
