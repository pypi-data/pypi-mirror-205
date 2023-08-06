from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


REQUIREMENTS = ['click']
SETUP_REQUIRES = ['flake8', 'pytest-runner']


setup(
    name='acnawebcli',
    version='0.1.0',
    description='CLI for study',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Antonio Carlos de Lima Junior',
    author_email='antonioclj.ac@gmail.com',
    url='https://github.com/acnaweb/cli-tools',
    packages=find_packages(include=['cli']),
    install_requires=REQUIREMENTS,
    setup_requires=SETUP_REQUIRES,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['greetings = cli.greeter:greet', 
                        'add = cli.calculator:add',
                        'subtract = cli.calculator:subtract',
                        'authenticate = cli.authenticate:auth',
                        'clitools = cli.main:main']
    },
    classifiers=[               
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',        
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: English',

      ],
    keywords='library test',
    license='MIT',
)
