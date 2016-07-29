from distutils.core import setup

setup(
    name='passe-partout',
    author='Benjamin Oertel',
    version='0.1dev',
    license='BSD',
    packages=['passepartout'],
    include_package_data=True,
    long_description=open('README.md').read(),
    install_requires=[
        'click == 6.6',
        'requests == 2.10.0',
    ],
    entry_points='''
        [console_scripts]
        passepartout=passepartout.cli:cli
    '''
)
