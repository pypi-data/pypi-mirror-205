from setuptools import setup, find_packages


setup(
    name='alxpytest',
    version='1',
    license='MIT',
    author="Marko Aleksov",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='example project',
    install_requires=[
          'pywin32',
      ],

)