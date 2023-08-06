from setuptools import setup, find_packages

setup(
    name="scraper-toolkit-pggm",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # List your module's dependencies here
    ],
    author="Dominique Stoverink",
    author_email="dominique.stoverink@pggm.nl",
    description="A toolkit module for the Mimir app created in Innovation Data Lab",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PGGM-Innovatie/scraper-toolkit-pggm",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
