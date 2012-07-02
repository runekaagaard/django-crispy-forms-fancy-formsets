# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from fancy_formsets import __version__


setup(
    name='django-crispy-forms-fancy-formsets',
    version=__version__,
    author='Rune Kaagaard',
    url='https://github.com/runekaagaard/django-crispy-forms-fancy-formsets',
    description='',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
