from setuptools import (
    setup,
    find_packages,
)
import sys

from bs4 import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="beautifulsoup4",
    version = __version__,
    author="Leonard Richardson",
    author_email='leonardr@segfault.org',
    url="https://www.crummy.com/software/BeautifulSoup/bs4/",
    download_url = "https://www.crummy.com/software/BeautifulSoup/bs4/download/",
    description="Screen-scraping library",
    python_requires='>=3.6.0',
    install_requires=[
        "soupsieve >1.2",
    ],
    tests_require=['pytest'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=['bs4', 'bs4/builder', 'bs4/tests'],
    # NOTE: Stuff like the documentation is included via MANIFEST.in
    extras_require = {
        'lxml' : [ 'lxml'],
        'html5lib' : ['html5lib'],
    },
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Python",
                 'Programming Language :: Python :: 3',
                 "Topic :: Text Processing :: Markup :: HTML",
                 "Topic :: Text Processing :: Markup :: XML",
                 "Topic :: Text Processing :: Markup :: SGML",
                 "Topic :: Software Development :: Libraries :: Python Modules",
             ],
)
