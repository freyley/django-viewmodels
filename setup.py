from setuptools import setup
import subprocess
import os.path

long_description = (open('README.rst').read() + 
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-viewmodels',
    version='0.1.0',
    description='Class based views for Django with automatic viewmodel rendering',
    author='Jeff Schwaber, Chris Pitzer, LoFi Art',
    author_email='freyley@gmail.com',
    long_description=long_description,
    url='',
    packages=['djviewmodels'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    #test_suite='tests.runtests.runtests',
    package_data={
        'djviewmodels': [
            '*.py',
        ]
    },
)
