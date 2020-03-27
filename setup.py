from setuptools import setup, find_packages
import os
import sys

directory = os.path.abspath(os.path.dirname(__file__))
if sys.version_info >= (3, 0):
    with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    with open(os.path.join(directory, 'README.md')) as f:
        long_description = f.read()

setup(name='GEO450_GRASS_S1',
      packages=find_packages(),
      include_package_data=True,
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      description='....', # missing
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
      ],
      install_requires=["pyroSAR"],
      python_requires='>=3.6.0',
      url='https://github.com/marlinmm/GEO450_GRASS_S1.git',
      author='', #'Jonas Ziemer', Marlin Mueller, Patrick Fischer  # how to add second author?
      author_email='',
      license='MIT',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')