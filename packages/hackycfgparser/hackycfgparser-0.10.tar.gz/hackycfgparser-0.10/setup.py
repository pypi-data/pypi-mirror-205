from setuptools import setup, find_packages
# import codecs
# import os
# 
# here = os.path.abspath(os.path.dirname(__file__))
# 
# with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Hacky config parser - parses ConfigParser-compatible files / sys.argv and changes the defaults of functions'''

# Setting up
setup(
    name="hackycfgparser",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/hackycfgparser',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['deepcopyall', 'flatten_any_dict_iterable_or_whatsoever', 'tolerant_isinstance'],
    keywords=['hacky', 'config', 'parser', 'decorator'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['deepcopyall', 'flatten_any_dict_iterable_or_whatsoever', 'tolerant_isinstance'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*