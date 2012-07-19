from os.path import join
import re
from setuptools import setup, find_packages


# dynamically pull the version from django_ace/__init__.py
version = re.search('^__version__ = "(.+?)"$',
                    open(join('prod_calendar', 
                                '__init__.py')).read(), 
                                                re.MULTILINE).group(1)

setup(
    name='django-prod-calendar',
    version=version,
    description='A production calendar and demand scheduler for django',
    long_description=open('README.rst').read(),

    author='Graeme Sutherland',
    author_email='grasuth@nodestone.com',
    license="Simplified BSD",
    url='https://github.com/grasuth/django-prod-calendar',

    packages=find_packages(),
    include_package_data=True,
    install_requires=['Django'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        ],
    )

