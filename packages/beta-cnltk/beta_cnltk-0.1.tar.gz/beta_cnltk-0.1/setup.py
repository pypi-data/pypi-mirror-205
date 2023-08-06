from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',

]

setup(
    name='beta_cnltk',
    version='0.1',
    description='This is the Beta version of the CNLTK library',
    long_description=open('README.md').read(),
    url='https://github.com/AG0nzales',
    author='Joshua Gonzales',
    author_email='iwagproject@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='NLP',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'CNLTK': ['*.h5', '*.pkl', '*.csv', 'config.ini'],
    },
    install_requires=['']
)
