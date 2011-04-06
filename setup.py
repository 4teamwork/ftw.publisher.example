from setuptools import setup, find_packages
import os

version = open('ftw/publisher/example/version.txt').read().strip()
maintainer = 'Jonas Baumann'

setup(name='ftw.publisher.example',
      version=version,
      description="Example workflow integration for ftw.publisher's " +\
          "staging and publishing system",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='ftw publisher example',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.publisher.example',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.publisher'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        ],

      extras_require={
        'sender': [
            'ftw.publisher.sender'
            ],
        'receiver': [
            'ftw.publisher.receiver'
            ],
        },

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
