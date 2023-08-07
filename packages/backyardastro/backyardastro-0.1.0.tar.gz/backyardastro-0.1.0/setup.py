from setuptools import setup, find_packages

setup(
    name="backyardastro",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for backyard astronomy",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "datetime",
        "astropy",
        "ephem",
        "pytz",
        "tzwhere",
        "astroquery",
        "scipy",
        "tqdm",
    ],
)
