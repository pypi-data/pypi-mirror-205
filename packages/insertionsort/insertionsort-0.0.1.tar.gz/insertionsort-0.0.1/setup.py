from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3"]

setup(name='insertionsort',
      version = '0.0.1',
      description="insertion and shell sort algorithms",
      long_description = open("README.txt").read(),
      url = '',
      author = "Filip Kulka",
      author_email = 'fifkul252@gmail.com',
      license = "MIT",
      classifiers = classifiers,
      keywords = 'insertionsort',
      packages = find_packages(),
      install_requires = ['']
      )