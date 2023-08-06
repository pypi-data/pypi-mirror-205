from setuptools import setup

setup(
    name = 'polstats',
    version = '0.1.0',
    description = 'polstats: polarization statistics',
    url = 'https://github.com/dennis-l/polstats',
    author = 'Dennis Lee',
    author_email = '',
    packages = ['polstats'],
    package_dir={'': 'src'},
    install_requires=[
        "numpy",
        "scipy",
        "astropy",
    ],
)
