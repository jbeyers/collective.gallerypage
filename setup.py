from setuptools import setup, find_packages
import os

version = "1.0"

setup(
    name="collective.gallerypage",
    version=version,
    description="A page with rich text and gallery functionality",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "framework :: plone5",
        "Programming Language :: Python3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="",
    author="",
    author_email="",
    url="https://github.com/jbeyers/collective.gallerypage",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot>=0.6.0",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
