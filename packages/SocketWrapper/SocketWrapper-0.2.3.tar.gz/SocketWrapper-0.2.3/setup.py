from distutils.core import setup
from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'SocketWrapper',         # How you named your package folder (MyLib)
  packages = ['SocketWrapper'],   # Chose the same as "name"
  version = '0.2.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Jarred',                   # Type in your name
  author_email = 'jarredtdesrosiers@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/JarredTD/Socket_Wrapper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JarredTD/Socket_Wrapper/archive/refs/tags/0.2.3.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[],        # I get to this in a second,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)