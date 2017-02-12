from os import path
from setuptools import setup
import pyoptmat

here = path.abspath(path.dirname(__file__))

# Get the long description from the RpythonEADME file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pyoptmat',
      version=pyoptmat.__version__,
      description='Definitions of dielectric constants of optical materials.',
      long_description=long_description,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='dielectric constant, optical material',
      author=pyoptmat.__author__,
      author_email='mnishida@hiroshima-u.ac.jp',
      url='https://github.com/mnishida/PyOptMat',
      license=pyoptmat.__license__,
      packages=['pyoptmat', 'tests'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'riip'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """
      )
