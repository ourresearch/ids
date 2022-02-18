from setuptools import setup

setup(
    name='ids',
    version='0.2.0',
    py_modules=['ids','tokens','unsub_database'],
    install_requires=[
        ['Click','pandas','redshift_connector','requests',],
    ],
    entry_points={
        'console_scripts': [
            'ids = ids:cli',
            'tokens = tokens:cli'
        ],
    },
)
