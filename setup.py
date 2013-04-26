from setuptools import setup, find_packages
import os

version = '1.1a'

zug_require = [
    'izug.basetheme',
    'ftw.contentmenu'
]

README = open("README.rst").read()
CHANGES = open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='seantis.dir.facility',
      version=version,
      description="Facility directory for seantis.reservation",
      long_description=README + '\n\n' + CHANGES,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone 4.3",
          "Programming Language :: Python",
      ],
      keywords='',
      author='Seantis GmbH',
      author_email='info@seantis.ch',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['seantis', 'seantis.dir'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone>=4.3',
          'plone.namedfile>=2.0.1',
          'plone.app.dexterity',
          'seantis.dir.base',
          'seantis.reservation',
          'collective.js.underscore',
          'collective.js.fullcalendar',
          'plone.namedfile'
          # -*- Extra requirements: -*-
      ],
      extras_require=dict(zug=zug_require),
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
