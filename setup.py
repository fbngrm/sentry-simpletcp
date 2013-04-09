#!/usr/bin/env python
from setuptools import setup, find_packages


tests_require = [
    'nose',
]

install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-simpletcp',
    version='0.0.1',
    author='Fabian Grimme',
    author_email='fabian@mixd.tv',
    url='http://github.com/getsentry/sentry-simpletcp',
    description='A Sentry extension which integrates a tcp connection to a given server.',
    long_description=__doc__,
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'github = sentry_simpletcp',
        ],
       'sentry.plugins': [
            'github = sentry_simpletcp.plugin:SimpleTCPPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
