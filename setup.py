from setuptools import setup, find_packages

version = '0.0'

setup(name='startupdrinks',
      version=version,
      description="",
      long_description="El portal de startupdrinks en mexico",
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[],
      keywords="grok zope",
      author="Noe Nieto",
      author_email="nnieto@noenieto.com",
      url="http://startupdrinks.mx/",
      license="GPL",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'grokui.admin',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.chameleon',
                        'grokcore.startup',
                        'plone.i18n',
                        'Pillow',
                        #Z3c.form madness
                        'zope.app.pagetemplate',
                        'megrok.pagetemplate',
                        'z3c.form',
                        'megrok.z3cform.base',
                        'megrok.z3cform.layout',
                        'dolmen.blob',
                        'dolmen.widget.file',
                        'dolmen.widget.image',
                        'dolmen.thumbnailer',
                        'plone.registry',
                        ],
      entry_points={
          'fanstatic.libraries': [
              'startupdrinks = startupdrinks.resource:library',
          ]
      })
