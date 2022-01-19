from setuptools import setup

setup(
    name='ids',
    version='0.1.0',
    py_modules=['ids','unsub_database'],
    install_requires=[
        ['Click','pandas','redshift_connector',],
    ],
    entry_points={
        'console_scripts': [
            'ids = ids:cli'
        ],
    },
)
