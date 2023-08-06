from setuptools import setup, find_packages

# reading long description from file
# with open('DESCRIPTION.txt') as file:
#     long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = [ 'os', 'sys', 'ImageTk', 'Image', 'messagebox', 'random', 'string', 'json' ]

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

# calling the setup function
setup(name='passLass498',
      version='1.0.0',
      description='A simple python wrapper for creating passwords..',
      long_description="A simple python wrapper for creating passwords",
      url='https://github.com/TheCodingFreakj/password-manager',
      download_url='https://github.com/TheCodingFreakj/password-manager/archive/refs/tags/passLass.tar.gz',
      author='Pallavi Priyadarshini',
      author_email='pallavidapriya75@gmail.com',
      license='MIT',
      # packages=[ 'password-manager' ],
      packages=find_packages('passLass498'),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='password manager'
      )
