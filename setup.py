from setuptools import find_packages, setup


VERSION = '0.0.0'


def read_requirements(path):
    return [
        line.strip()
        for line in read_file(path).split('\n')
        if line.strip() and
        not line.startswith('#')]


def read_file(path):
    with open(path) as fh:
        return fh.read()


setup(
    name='mlog',
    version=VERSION,
    description='A minimal static blog generator',
    long_description=read_file('README'),
    url='https://github.com/justinfay/mlog',
    author='Justin Fay',
    author_email='mail@justinfay.me',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: web blog',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='static blog generator',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    package_data={
        'templates': 'mlog/templates/*',
        'static': 'mlog/static/*',
    },
    entry_points={
        'console_scripts': [],
    })
