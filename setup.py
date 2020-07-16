from setuptools import setup

setup(name='twop',
      version='0.1',
      description='TaskWarrior OpenProject Sync',
      url='https://github.com/flippipe/twop',
      author='🐧Flip',
      author_email='filipe@quercus.club',
      license='GPLv3',
      packages=['twop'],
      scripts=['bin/twop.sh'],
      zip_safe=False)
